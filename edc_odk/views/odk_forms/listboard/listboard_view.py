import os
import requests
from django.apps import apps as django_apps
from django.core.exceptions import MultipleObjectsReturned
from django.contrib import messages
from django.db.utils import IntegrityError
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import ListboardView as BaseListboardView
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_navbar import NavbarViewMixin
from edc_base.utils import get_utcnow
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET

from edc_odk.model_wrappers import ConsentCopiesModelWrapper
from edc_odk.conn_options import ODKConnectionOptions


class ListboardView(EdcBaseViewMixin, NavbarViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin,
                    BaseListboardView):

    listboard_template = 'odk_listboard_template'
    listboard_url = 'odk_listboard_url'
    listboard_panel_style = 'success'
    listboard_fa_icon = "fa fa-file-image"

    model = 'edc_odk.consentcopies'
    model_wrapper_cls = ConsentCopiesModelWrapper
    navbar_name = 'edc_odk_forms'
    navbar_selected_item = 'edc_odk_forms'
    search_form_url = 'odk_listboard_url'
    conn_options = ODKConnectionOptions

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        return options

    def get_context_data(self, **kwargs):
        final_count = 0
        consent_records = 0
        clinician_notes_records = 0

        if self.request.GET.get('pull_data'):
            consent_records += self.pull_consent_images_data()
            clinician_notes_records += self.pull_clinician_notes_data()
            final_count = consent_records + clinician_notes_records

            if final_count > 0:
                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    f'{final_count} record(s) downloaded successfully from the '
                    f'odk aggregrate server, {consent_records} consent copie(s) '
                    f'and {clinician_notes_records} clinician notes copie(s).')
            else:
                messages.add_message(
                    self.request,
                    messages.INFO,
                    f'No new records found from the odk aggregrate.')
        context = super().get_context_data(**kwargs)

        return context

    def pull_data_from_odk(self, form_id=None):
        # Get connection options from settings conf
        host = self.conn_options.host
        user = self.conn_options.user
        pw = self.conn_options.password

        base_format = 'http://%(host)s/view/%(api)s?formId=%(form_id)s'
        submission_format = '[@version=null and @uiVersion=null]/%(group_name)s[@key=%(uuid)s]'

        auth = HTTPDigestAuth(user, pw)
        result = requests.get(base_format % {'form_id': form_id,
                                             'api': 'submissionList',
                                             'host': host},
                              auth=auth)
        root = ET.fromstring(result.text)
        results = []
        if len(root) > 1:
            idlist, _ = [child for child in root]
            for uuid in [i.text for i in idlist]:
                result = []
                url = (base_format % {'form_id': form_id,
                                      'api': 'downloadSubmission',
                                      'host': host} +
                       submission_format % {'group_name': 'data',
                                            'uuid': uuid})
                reply = requests.get(url, auth=auth)
                root = ET.fromstring(reply.text)

                child = [child for child in root]
                subject_identifier = None
                for data in child:
                    content = data.tag.replace(
                        '{http://opendatakit.org/submissions}', '')
                    if content == 'data':
                        elemlist = list(data[0][0])
                        for info in elemlist:
                            if 'subject_identifier' in info.tag:
                                subject_identifier = info.text
                            result.append(
                                dict([(info.tag.replace(
                                    '{http://opendatakit.org/submissions}', ''),
                                    info.text)]))

                    elif content == 'mediaFile':
                        elemlist = list(data)

                        filename = elemlist[0].text
                        downloadUrl = elemlist[2].text
                        key = None
                        timestamp = get_utcnow()
                        timestamp = timestamp.strftime("%Y%m%d_%H%M%S%f")

                        image_groups = [
                            'subject_omang', 'subject_consent',
                            'specimen_consent', 'clinician_notes']
                        for group in image_groups:
                            if group in downloadUrl:
                                key = group
                                file_ext = os.path.splitext(filename)[1]
                                filename = '%s-%s-image-%s%s' % (
                                    subject_identifier, group, timestamp, file_ext)

                        result.append(
                            dict([('%s' % key, [filename, downloadUrl])]))
                results.append(result)

        return results

    def pull_consent_images_data(self):
        result = self.pull_data_from_odk(form_id='consent_forms')
        img_cls = {'subject_consent': self.consent_image_model_cls,
                   'subject_omang': self.national_id_image_model_cls,
                   'specimen_consent': self.specimen_consent_image_model_cls}

        return self.populate_model_objects(
            None,
            result,
            django_apps.get_model(self.model),
            img_cls,
            'consent_copies',
            subject_identifier=None,
            consent_version=None,
            subject_consent=None,
            subject_omang=None,
            specimen_consent=None)

    def pull_clinician_notes_data(self):
        form_ids = self.get_clinician_notes_form_id()
        record_count = 0

        for app_name, form_id in form_ids.items():
            img_cls = django_apps.get_model(
                self.clinician_notes_image_model(app_name))

            result = self.pull_data_from_odk(form_id=form_id)

            record_count += self.populate_model_objects(
                app_name,
                result,
                self.clinician_notes_model_cls(app_name),
                img_cls,
                'clinician_notes',
                subject_identifier=None,
                visit_code=None,
                timepoint=None,
                clinician_notes=None)
        return record_count

    def populate_model_objects(
            self, app_name, result, model_cls, image_cls, image_cls_field, **fields):
        count = 0
        for data in result:

            data_dict = dict()

            index = 0
            while index < len(data):
                for field in fields.keys():
                    if field in data[index].keys():
                        data_dict.update(
                            {field: data[index].get(field)})
                        if isinstance(data_dict.get(field), list):
                            data_dict.setdefault(
                                '%s_image_name' % field, []).append(
                                    data[index].get(field)[0])

                            data_dict.setdefault(
                                '%s_image_url' % field, []).append(
                                    data[index].get(field)[1])
                index += 1

            if data_dict.get('visit_code'):
                # Get visit
                visit_obj = self.get_app_visit_model_obj(
                    app_name,
                    data_dict.get('subject_identifier'),
                    data_dict.get('visit_code'),
                    data_dict.get('timepoint'))

                model_cls = model_cls

                visit_models = self.get_visit_models().get(app_name)
                field_name = visit_models[0]

                if visit_obj:
                    try:
                        obj, created = model_cls.objects.get_or_create(
                            report_datetime=visit_obj.report_datetime,
                            **{f'{field_name}': visit_obj})

                        if created:
                            self.create_image_obj_upload_image(
                                image_cls,
                                image_cls_field,
                                obj,
                                data_dict)

                            count += 1

                    except (MultipleObjectsReturned, IntegrityError) as e:
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            e)

            elif data_dict.get('subject_identifier'):
                try:
                    obj, created = model_cls.objects.get_or_create(
                        subject_identifier=data_dict.get('subject_identifier'),
                        version=data_dict.get('consent_version'))
                    if created:
                        self.create_image_obj_upload_image(
                            image_cls,
                            image_cls_field,
                            obj,
                            data_dict)

                        count += 1
                except (MultipleObjectsReturned, IntegrityError) as e:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        e)

        return count

    def create_image_obj_upload_image(
            self, images_cls, field_name, obj, fields):
        image_names = [field for field in fields.keys() if 'image_name' in field]
        image_urls = [field for field in fields.keys() if 'image_url' in field]

        result = zip(image_names, image_urls)
        image_cls = None

        for image_name, image_url in result:
            if isinstance(images_cls, dict):
                image_cls = images_cls.get(
                    image_name.replace('_image_name', ''))
            else:
                image_cls = images_cls

            i = 0
            while i < len(fields.get(image_name)):
                image_cls.objects.create(
                    **{f'{field_name}': obj},
                    image=fields.get(image_name)[i])

                # Download and upload image
                self.download_image_file_upload(
                    fields.get(image_url)[i],
                    fields.get(image_name)[i])
                i += 1

    def download_image_file_upload(self, downloadUrl, filename):
        r = requests.get(downloadUrl, stream=True)
        if r.status_code == 200:
            with open('media/%(filename)s' % {'filename': filename}, 'wb') as f:
                f.write(r.content)

    def get_app_visit_model_obj(
            self, app_name, subject_identifier, visit_code, timepoint):
        visit_model_obj = None
        visit_models = self.get_visit_models().get(app_name)

        if visit_models:
                visit_model_cls = django_apps.get_model(
                    visit_models[1])
                try:
                    visit_model_obj = visit_model_cls.objects.get(
                        subject_identifier=subject_identifier,
                        visit_code=visit_code,
                        visit_code_sequence=timepoint)
                except visit_model_cls.DoesNotExist:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        f'Failed to get visit for {subject_identifier}, at '
                        f'visit {visit_code}. Visit does not exist.')

        return visit_model_obj

    def get_visit_models(self):
        app_config = django_apps.get_app_config('edc_visit_tracking')
        return app_config.visit_models

    def get_clinician_notes_form_id(self):
        app_config = django_apps.get_app_config('edc_odk')
        return app_config.clinician_notes_form_ids

    @property
    def consent_image_model_cls(self):
        consent_image_model = 'edc_odk.consentimage'
        return django_apps.get_model(consent_image_model)

    @property
    def specimen_consent_image_model_cls(self):
        specimen_consent_image_model = 'edc_odk.specimenconsentimage'
        return django_apps.get_model(specimen_consent_image_model)

    @property
    def national_id_image_model_cls(self):
        nation_id_image_model = 'edc_odk.nationalidentityimage'
        return django_apps.get_model(nation_id_image_model)

    def clinician_notes_image_model(self, app_name=None):
        return '%s.cliniciannotesimage' % app_name

    def clinician_notes_model_cls(self, app_name=None):
        app_config = django_apps.get_app_config(
            'edc_odk').clinician_notes_models

        clinician_notes_model = app_config.get(app_name, 'default')

        if clinician_notes_model:
            return django_apps.get_model(
                '%s.%s' % (app_name, clinician_notes_model))

import configparser
import os
import requests
import xml.etree.ElementTree as ET
import logging
import PIL
import pytz


from dateutil.parser import parse
from django.conf import settings
from django.apps import apps as django_apps
from django.db.utils import IntegrityError
from django.db.models import ManyToOneRel, Q
from edc_appointment.constants import NEW_APPT
from edc_base.utils import get_utcnow
from requests.auth import HTTPDigestAuth
from PIL import Image


logger = logging.getLogger(__name__)


class PullODKData:
    """
    Pull image copies from the odk server, create relevant model objects.
    """

    base_format = settings.BASE_FORMAT
    submission_format = '[@version=null and @uiVersion=null]/%(group_name)s[@key=%(uuid)s]'

    def __init__(self, request=None):
        self.host, self.user, self.pswd = self.connection_options()
        self.request = request

    def connection_options(self):
        credentials = list()
        config = configparser.ConfigParser()

        settings_dict = settings.ODK_CONFIGURATION
        config_file = settings_dict['OPTIONS'].get('read_default_file')
        config.read(config_file)
        if config_file:
            credentials.append(config['read']['host'])
            credentials.append(config['read']['user'])
            credentials.append(config['read']['pw'])
        return credentials

    def connect_to_odk_server(self, url=None):
        """
        Send GET request to the odk aggregate server, to download submissions
        data
        @param url: url request.
        @return: requests.Response string parsed into an Element
        """
        auth = HTTPDigestAuth(self.user, self.pswd)

        try:
            result = requests.get(url, auth=auth)
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise Exception(f'HTTP Error {err}')
        except requests.exceptions.ConnectionError as cerr:
            raise Exception(f'Error Connecting: {cerr}')
        except requests.exceptions.RequestException as rexc:
            raise Exception(
                f'An error occurred while trying to get data {rexc}')
        else:
            return ET.fromstring(result.text)

    def download_submissions_data(self, form_id=None):
        """
        Download form submissions data and construct results dictionary.
        @param form_id: id of the form as defined on the odk form design
        @return: results dict
        """
        submissions_url = (self.base_format % {'form_id': form_id,
                                               'api': 'submissionList',
                                               'host': self.host})
        root = self.connect_to_odk_server(url=submissions_url)
        results = []
        if len(root) > 1:
            idlist, _ = [child for child in root]
            for uuid in [i.text for i in idlist]:
                result = []
                url = (self.base_format % {'form_id': form_id,
                                           'api': 'downloadSubmission',
                                           'host': self.host} +
                       self.submission_format % {'group_name': 'data',
                                                 'uuid': uuid})

                root = self.connect_to_odk_server(url=url)

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
                            'specimen_consent', 'clinician_notes',
                            'notes_to_file', 'lab_results']
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
        result = self.download_submissions_data(form_id='consent_forms')
        img_cls = self.consent_image_model_cls

        return self.populate_model_objects(
            None,
            result,
            django_apps.get_model('edc_odk.consentcopies'),
            img_cls,
            'consent_copies',
            subject_identifier=None,
            consent_version=None,
            subject_consent=None)

    def pull_specimen_consent_images_data(self):
        result = self.download_submissions_data(
            form_id='specimen_consent_forms')
        img_cls = self.specimen_consent_image_model_cls

        return self.populate_model_objects(
            None,
            result,
            django_apps.get_model('edc_odk.specimenconsentcopies'),
            img_cls,
            'consent_copies',
            subject_identifier=None,
            specimen_consent=None)

    def pull_omang_images_data(self):
        result = self.download_submissions_data(form_id='omang_forms')
        img_cls = self.national_id_image_model_cls

        return self.populate_model_objects(
            None,
            result,
            django_apps.get_model('edc_odk.omangcopies'),
            img_cls,
            'omang_copies',
            subject_identifier=None,
            subject_omang=None)

    def pull_note_to_file_data(self):
        result = self.download_submissions_data(form_id='notes_to_file_v1.0')
        img_cls = self.note_to_file_image_model_cls

        return self.populate_model_objects(
            None,
            result,
            django_apps.get_model('edc_odk.notetofile'),
            img_cls,
            'notes_to_file',
            subject_identifier=None,
            notes_to_file=None)

    def pull_clinician_notes_data(self):
        form_ids = self.get_clinician_notes_form_id()
        record_count = 0
        record_updated = 0

        for app_name, form_id in form_ids.items():
            img_cls = django_apps.get_model(
                self.clinician_notes_image_model(app_name))

            result = self.download_submissions_data(form_id=form_id)

            count, updated = self.populate_model_objects(
                app_name,
                result,
                self.clinician_notes_model_cls(app_name),
                img_cls,
                'clinician_notes',
                subject_identifier=None,
                visit_code=None,
                timepoint=None,
                clinician_notes=None)
            record_count += count
            record_updated += updated
        return record_count, record_updated

    def pull_labresults_data(self):
        form_ids = self.get_labresults_form_id()
        record_count = 0
        record_updated = 0

        for app_name, form_id in form_ids.items():
            img_cls = django_apps.get_model(
                self.labresults_file_model(app_name))

            result = self.download_submissions_data(form_id=form_id)

            count, updated = self.populate_model_objects(
                app_name,
                result,
                self.labresults_model_cls(app_name),
                img_cls,
                'lab_results',
                subject_identifier=None,
                visit_code=None,
                timepoint=None,
                lab_results=None)
            record_count += count
            record_updated += updated
        return record_count, record_updated

    def populate_model_objects(
            self, app_name, result, model_cls, image_cls, image_cls_field, **fields):
        updated = 0
        count = 0
        audit_fields = {'username': None,
                        'date_captured': None}
        fields.update(audit_fields)
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
                            report_datetime__gte=visit_obj.report_datetime,
                            **{f'{field_name}': visit_obj},
                            defaults={'report_datetime': visit_obj.report_datetime})
                        if created:
                            self.create_image_obj_upload_image(
                                image_cls,
                                image_cls_field,
                                obj,
                                data_dict)

                            count += 1
                        else:
                            imgs_updated = self.update_existing_image_objs(
                                image_cls,
                                image_cls_field,
                                obj,
                                data_dict)
                            if imgs_updated:
                                updated += 1

                    except IntegrityError as e:
                        raise Exception(e)

            elif data_dict.get('subject_identifier'):
                try:
                    if data_dict.get('consent_version'):
                        obj, created = model_cls.objects.get_or_create(
                            subject_identifier=data_dict.get('subject_identifier'),
                            version=data_dict.get('consent_version'))
                    else:
                        obj, created = model_cls.objects.get_or_create(
                            subject_identifier=data_dict.get('subject_identifier'))
                    if created:
                        self.create_image_obj_upload_image(
                            image_cls,
                            image_cls_field,
                            obj,
                            data_dict)
                        count += 1
                    else:
                        imgs_updated = self.update_existing_image_objs(
                            image_cls,
                            image_cls_field,
                            obj,
                            data_dict)
                        if imgs_updated:
                            updated += 1

                except IntegrityError as e:
                    raise Exception(e)
            else:
                obj, created = model_cls.objects.get_or_create(
                    identifier=data_dict.get('identifier'))
                if created:
                    self.create_image_obj_upload_image(
                        image_cls,
                        image_cls_field,
                        obj,
                        data_dict)

        return count, updated

    def update_existing_image_objs(self, images_cls, field_name, obj, fields):
        existing_datetime = self.recent_image_obj_datetime(
            images_cls, field_name, obj, fields)
        if existing_datetime:
            if parse(fields.get('date_captured')) > existing_datetime:
                self.create_image_obj_upload_image(images_cls, field_name, obj, fields)
            return True
        else:
            return False

    def recent_image_obj_datetime(self, images_cls, field_name, obj, fields):
        recent_captured = list()
        related_images = [field.get_accessor_name() for field in
                          obj._meta.get_fields() if issubclass(type(field), ManyToOneRel)]

        for related_image in related_images:
            recent_obj = getattr(
                obj, related_image).order_by('-datetime_captured').first()
            if recent_obj:
                recent_captured.append(recent_obj.datetime_captured)
            else:
                self.create_image_obj_upload_image(
                    images_cls, field_name, obj, fields)

        return max(recent_captured) if recent_captured else False

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

                upload_to = image_cls.image.field.upload_to

                # Check if path is func or string
                upload_to = upload_to(None, None) if callable(upload_to) else upload_to

                # Download and upload image
                download_success = self.download_image_file_upload(
                    fields.get(image_url)[i],
                    fields.get(image_name)[i],
                    upload_to)

                if download_success:
                    datetime_captured = parse(fields.get('date_captured'))
                    local_timezone = pytz.timezone('Africa/Gaborone')
                    datetime_captured.astimezone(local_timezone)
                    # create image model object
                    image_cls.objects.create(
                        **{f'{field_name}': obj},
                        image=upload_to + fields.get(image_name)[i],
                        user_uploaded=fields.get('username'),
                        datetime_captured=datetime_captured)

                    # Add a stamp to the image upload
                    path = 'media/%(upload_dir)s%(filename)s' % {
                        'filename': fields.get(image_name)[i],
                        'upload_dir': upload_to}
                    self.add_image_stamp(image_path=path)
                    i += 1

    def download_image_file_upload(self, downloadUrl, filename, upload_to):
        auth = HTTPDigestAuth(self.user, self.pswd)
        r = requests.get(downloadUrl, auth=auth, stream=True)
        image_path = 'media/%(upload_dir)s' % {'upload_dir': upload_to}
        if r.status_code == 200:
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            with open('%(path)s%(filename)s' % {'path': image_path, 'filename': filename}, 'wb') as f:
                f.write(r.content)
            return True
        else:
            r.raise_for_status()

    def get_app_visit_model_obj(
            self, app_name, subject_identifier, visit_code, timepoint):
        visit_model_obj = None
        visit_models = self.get_visit_models().get(app_name)

        if visit_models:
            visit_model_cls = django_apps.get_model(
                visit_models[1])

            visit_model_obj = visit_model_cls.objects.filter(
                subject_identifier=subject_identifier,
                visit_code=visit_code,
                visit_code_sequence=timepoint).exclude(
                    appointment__appt_status=NEW_APPT).order_by('-report_datetime').last()
            if not visit_model_obj:
                message = (f'Failed to get visit for {subject_identifier}, at '
                           f'visit {visit_code}. Visit does not exist.')
                logger.error(message)

        return visit_model_obj

    def get_visit_models(self):
        app_config = django_apps.get_app_config('edc_visit_tracking')
        return app_config.visit_models

    def get_clinician_notes_form_id(self):
        app_config = django_apps.get_app_config('edc_odk')
        return app_config.clinician_notes_form_ids

    def get_labresults_form_id(self):
        app_config = django_apps.get_app_config('edc_odk')
        return app_config.labresults_form_ids

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

    @property
    def note_to_file_image_model_cls(self):
        note_to_file_image_model = 'edc_odk.notetofiledocs'
        return django_apps.get_model(note_to_file_image_model)

    def clinician_notes_image_model(self, app_name=None):
        return '%s.cliniciannotesimage' % app_name

    def labresults_file_model(self, app_name=None):
        return '%s.labresultsfile' % app_name

    def clinician_notes_model_cls(self, app_name=None):
        app_config = django_apps.get_app_config(
            'edc_odk').clinician_notes_models

        clinician_notes_model = app_config.get(app_name, 'default')

        if clinician_notes_model:
            return django_apps.get_model(
                '%s.%s' % (app_name, clinician_notes_model))

    def labresults_model_cls(self, app_name=None):
        app_config = django_apps.get_app_config('edc_odk').labresults_models

        labresults_model = app_config.get(app_name, None)

        if labresults_model:
            return django_apps.get_model(
                '%s.%s' % (app_name, labresults_model))

    def add_image_stamp(self, image_path=None, position=(25, 25), resize=(600, 600)):
        """
        Superimpose image of a stamp over copy of the base image
        @param image_path: dir to base image
        @param position: pixels(w,h) to superimpose stamp at
        """
        base_image = Image.open(image_path)
        stamp = Image.open('media/stamp/true-copy.png')
        if resize:
            stamp = stamp.resize(resize, PIL.Image.ANTIALIAS)

        width, height = base_image.size
        stamp_width, stamp_height = stamp.size

        # Determine orientation of the base image before pasting stamp
        if width < height:
            pos_width = round(width/2)-round(stamp_width/2)
            pos_height = height-stamp_height
            position = (pos_width, pos_height)
        elif width > height:
            stamp = stamp.rotate(90)
            pos_width = width-stamp_width
            pos_height = round(height/2)-round(stamp_height/2)
            position = (pos_width, pos_height)

        # paste stamp over image
        base_image.paste(stamp, position, mask=stamp)
        base_image.save(image_path)

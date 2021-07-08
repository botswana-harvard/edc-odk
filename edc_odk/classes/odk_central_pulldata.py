import configparser
import requests
import json
import os

from django.apps import apps as django_apps
from django.conf import settings
from django.db.utils import IntegrityError
from edc_base.utils import get_utcnow

from .pull_odk_data import PullODKData


class ODKCentralPullData(PullODKData):
    """
    Pull image copies from the odk central server, create relevant model objects.
    """

    base_format = settings.BASE_FORMAT
    attachment_format = 'https://%(host)s/v1/projects/2/forms/%(form_id)s/%(api)s/%(instance_id)s/attachments'

    def __init__(self, request=None):
        self.central_url, self.central_email, self.central_password = self.connection_options()
        self.request = request

    def connection_options(self):
        """
        Construct the connection options as defined from the app config
        """
        credentials = list()
        config = configparser.ConfigParser()

        settings_dict = settings.ODK_CONFIGURATION
        config_file = settings_dict['OPTIONS'].get('read_default_file')
        config.read(config_file)
        if config_file:
            credentials.append(config['read']['central_url'])
            credentials.append(config['read']['central_email'])
            credentials.append(config['read']['central_password'])
        return credentials

    def connect_to_odk_server(self, url=None):
        """
        Send GET request to the odk central server, to download submissions
        data
        @param url: url request.
        @return: requests.Response string parsed to json
        """
        session_token = self.get_email_token()
        if session_token:
            response = requests.get(
                url, headers={"Authorization": "Bearer " + session_token})
            if response.status_code == 200:
                return response.json()
            else:
                print('Error connecting to server.')
        else:
            print('Error getting token')

    def get_email_token(self):
        """
        Verify user email and password, to create new email session and a bearer
        token.
        @return: bearer token (expiration: 24hrs)
        """
        email_token_response = requests.post(
            'https://' + self.central_url + '/v1/sessions',
            data=json.dumps({'email': self.central_email,
                             'password': self.central_password}),
            headers={"Content-Type": "application/json"},
        )

        if email_token_response.status_code == 200:
            return email_token_response.json()["token"]
        return None

    def download_submissions_data(self, form_id=None):
        """
        Download form submissions data and return response dictionary.
        @param form_id: id of the form as defined on the odk form design
        @return: response value dict
        """
        url = (self.base_format % {'form_id': f'{form_id}.svc',
                                   'api': 'Submissions',
                                   'host': self.central_url})

        response = self.connect_to_odk_server(url)
        if response:
            return response['value']
        else:
            return []

    def build_attachments_data(self, form_id=None, instance_id=None,
                               subject_identifier=None):
        """
        Download form submissions attachments and construct media dictionary.
        @param form_id: id of the form as defined on the odk form design
        @param instance_id: id of the submission record instance
        @param subject_identifier: pid of the record submission
        @return: media dict: {media_name: media_url}
        """
        attachments_url = self.attachment_format % {'form_id': form_id,
                                                    'api': 'submissions',
                                                    'instance_id': instance_id,
                                                    'host': self.central_url}
        attachments = self.connect_to_odk_server(attachments_url)
        timestamp = get_utcnow()
        timestamp = timestamp.strftime("%Y%m%d_%H%M%S%f")
        media_dict = {}
        if attachments:
            counter = 0
            for attachment in attachments:
                if attachment.get('exists'):
                    filename = attachment.get('name')
                    file_ext = os.path.splitext(filename)[1]
                    media_url = attachments_url + '/' + filename
                    filename = '%s-image%s-%s%s' % (
                        subject_identifier, counter, timestamp, file_ext)
                    media_dict.update({filename: media_url})
                counter += 1
        return media_dict

    def build_forms_data(self, results=[], form_id=None, media_group='',
                         include=None):
        """
        Format form submissions data into a dictionary with only required fields
        defined from include.
        @param results: submissions data pulled from the central server
        @param form_id: id of the form as defined on the odk form design
        @param media_group: name of the media attachments to expect
        @param: include: fields to include in the resulting dictionary
        @return: forms_data: [{x:y},{z:a}] -> list of submission records
        """
        forms_data = []
        audit_fields = ('date_captured', )
        include = include + audit_fields
        for result_data in results:
            system_meta = result_data.get('__system')
            form_meta = result_data.get('meta', '')
            instance_id = form_meta.get('instanceID', '') if form_meta else ''
            result_data = {k: result_data[k] for k in result_data.keys() & include}
            if system_meta:
                result_data['username'] = system_meta.get('submitterName')
            subject_identifier = result_data.get('subject_identifier')
            result_data[media_group] = self.build_attachments_data(
                form_id, instance_id, subject_identifier)
            forms_data.append(result_data)
        return forms_data

    def pull_consent_images_data(self):
        img_cls = self.consent_image_model_cls
        fields_include = ('subject_identifier', 'consent_version',
                          'subject_consent', )
        results = self.download_submissions_data(form_id='consent_forms')
        results = [result for result in results if result['__system']['reviewState'] != 'rejected']
        results_fmt = self.build_forms_data(
            results=results,
            form_id='consent_forms',
            media_group='consent_copies',
            include=fields_include)

        return self.populate_model_objects(
            None,
            results_fmt,
            django_apps.get_model('edc_odk.consentcopies'),
            img_cls,
            'consent_copies')

    def pull_specimen_consent_images_data(self):
        img_cls = self.specimen_consent_image_model_cls
        fields_include = ('subject_identifier', 'specimen_consent', )
        results = self.download_submissions_data(form_id='specimen_consent_forms')
        results = [result for result in results if result['__system']['reviewState'] != 'rejected']
        results_fmt = self.build_forms_data(
            results=results,
            form_id='specimen_consent_forms',
            media_group='consent_copies',
            include=fields_include)

        return self.populate_model_objects(
            None,
            results_fmt,
            django_apps.get_model('edc_odk.specimenconsentcopies'),
            img_cls,
            'consent_copies')

    def pull_omang_images_data(self):
        img_cls = self.national_id_image_model_cls
        fields_include = ('subject_identifier', 'subject_omang', )
        results = self.download_submissions_data(form_id='omang_forms')
        results = [result for result in results if result['__system']['reviewState'] != 'rejected']
        results_fmt = self.build_forms_data(
            results=results,
            form_id='omang_forms',
            media_group='omang_copies',
            include=fields_include)

        return self.populate_model_objects(
            None,
            results_fmt,
            django_apps.get_model('edc_odk.omangcopies'),
            img_cls,
            'omang_copies')

    def pull_clinician_notes_data(self):
        form_ids = self.get_clinician_notes_form_id()
        record_count = 0
        record_updated = 0
        fields_include = ('subject_identifier', 'visit_code', 'timepoint')
        for app_name, form_id in form_ids.items():
            img_cls = django_apps.get_model(self.clinician_notes_image_model(app_name))

            results = self.download_submissions_data(form_id=form_id)
            results = [result for result in results if result['__system']['reviewState'] != 'rejected']
            results_fmt = self.build_forms_data(
                results=results, form_id=form_id,
                media_group='clinician_notes',
                include=fields_include)
            count, updated = self.populate_model_objects(
                app_name,
                results_fmt,
                self.clinician_notes_model_cls(app_name),
                img_cls,
                'clinician_notes')
            record_count += count
            record_updated += updated
        return record_count, record_updated

    def populate_model_objects(self, app_name, result, model_cls, image_cls,
                               image_cls_field):
        updated = 0
        count = 0
        for data_dict in result:
            if data_dict.get('visit_code'):
                # Get visit
                visit_obj = self.get_app_visit_model_obj(
                    app_name,
                    data_dict.get('subject_identifier'),
                    data_dict.get('visit_code'),
                    data_dict.get('timepoint'))

                visit_models = self.get_visit_models().get(app_name)
                field_name = None
                if visit_models:
                    field_name = visit_models[0]
                if visit_obj:
                    try:
                        obj, created = model_cls.objects.get_or_create(
                            report_datetime__gte=visit_obj.report_datetime,
                            **{f'{field_name}': visit_obj})
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
        return count, updated

    def create_image_obj_upload_image(self, images_cls, field_name, obj, data_dict):
        media_info = data_dict.get(field_name)
        upload_to = images_cls.image.field.upload_to
        for media_name, media_url in media_info.items():

            # Download and upload image
            download_success = self.download_image_file_upload(
                media_url,
                media_name,
                upload_to)

            if download_success:
                # create image model object
                images_cls.objects.create(
                    **{f'{field_name}': obj},
                    image=upload_to + media_name,
                    user_uploaded=data_dict.get('username'),
                    datetime_captured=data_dict.get('date_captured'))

                # Add a stamp to the image upload
                path = 'media/%(upload_dir)s%(filename)s' % {
                    'filename': media_name,
                    'upload_dir': upload_to}
                self.add_image_stamp(image_path=path, resize=(100, 100))

    def download_image_file_upload(self, downloadUrl, filename, upload_to):
        session_token = self.get_email_token()
        image_path = 'media/%(upload_dir)s' % {'upload_dir': upload_to}
        if session_token:
            resp = requests.get(downloadUrl,
                                headers={"Authorization": "Bearer " + session_token},
                                stream=True)
            if resp.status_code == 200:
                if not os.path.exists(image_path):
                    os.makedirs(image_path)
                with open('%(path)s%(filename)s' % {
                        'path': image_path, 'filename': filename}, 'wb') as f:
                    f.write(resp.content)
                return True
            else:
                resp.raise_for_status()

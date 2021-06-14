from django.apps import apps
from unittest.mock import patch
from django.test import TestCase
from edc_base.utils import get_utcnow

from ..classes import ODKCentralPullData
from .models import Appointment, ClinicianNotes, ClinicianNotesImage, SubjectVisit


class TestCreateModelInstance(TestCase):

    def setUp(self):
        subject_identifier = '12356'
        visit_code = '2000M'
        timepoint = '0'
        appointment = Appointment.objects.create(
            subject_identifier=subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code=visit_code)

        self.subject_visit = SubjectVisit.objects.create(
            report_datetime=get_utcnow(),
            appointment=appointment,
            subject_identifier=subject_identifier,
            visit_code=visit_code,
            visit_code_sequence=timepoint)

        self.odk_central_data = [
            {
                'subject_identifier': '12356',
                'visit_code': visit_code,
                'timepoint': timepoint,
                'date_captured': '2021-06-10T10:05:38.063+02:00',
                'username': 'ame',
                'clinician_notes': {
                    'test_image1.png':
                    'https://homepages.cae.wisc.edu/~ece533/images/airplane.png',
                    'test_image2.png':
                    'https://homepages.cae.wisc.edu/~ece533/images/arctichare.png'
                }
            }
        ]

    def test_model_obj_populates_data(self):
        """
        Assert if relevant model object is created successfully, when data from
        the odk server is passed.
        """
        with patch.object(apps.get_app_config('edc_visit_tracking'), 'visit_models',
                          new={'edc_odk': ('subjectvisit', 'edc_odk.subjectvisit')}):
            app_name = 'edc_odk'
            ODKCentralPullData().populate_model_objects(
                app_name, self.odk_central_data, ClinicianNotes,
                ClinicianNotesImage, 'clinician_notes')
        self.assertEqual(ClinicianNotes.objects.count(), 1)

    def test_media_model_obj_upload(self):
        """
        Assert if related media model objects are created successfully, with
        url data from the odk server passed.
        """
        clinician_notes = ClinicianNotes.objects.create(
            report_datetime=get_utcnow(),
            subjectvisit=self.subject_visit)
        ODKCentralPullData().create_image_obj_upload_image(
            ClinicianNotesImage, 'clinician_notes', clinician_notes,
            self.odk_central_data[0])
        self.assertEqual(ClinicianNotesImage.objects.count(), 2)

    def test_image_download(self):
        url = 'https://homepages.cae.wisc.edu/~ece533/images/airplane.png'
        name = 'test_image.png'
        upload_to = 'test_images/'

        self.assertTrue(
            ODKCentralPullData().download_image_file_upload(url, name, upload_to))

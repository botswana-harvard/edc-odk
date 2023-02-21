from django.apps import apps as django_apps

from .reportmixin import ReportMixin
from ..models import *


class AdultReports(ReportMixin):
    app_config = django_apps.get_app_config('edc_odk')
    consent_model = app_config.adult_consent_model

    @property
    def missing_parental_consent(self):
        return self.check_missing(ParentalConsent, 'parental_consent_images')

    @property
    def missing_omang_copies(self):
        return self.check_missing(OmangCopies, 'national_id_images')

    @property
    def missing_adult_main_consent(self):
        return self.check_missing(AdultMainConsent, 'adult_main_consent_images')

    @property
    def missing_note_to_files(self):
        return self.check_missing(NoteToFile, 'note_to_file')

    @property
    def missing_lab_results_files(self):
        return self.check_missing(LabResultsFiles, 'lab_results')

    @property
    def missing_clinician_notes_archives(self):
        return self.check_missing(ClinicianNotesArchives, 'clinician_notes_archives')

    @property
    def missing_consent_copies(self):
        return self.check_missing(ConsentCopies, 'consent_images')

    @property
    def missing_specimen_consent_copies(self):
        return self.check_missing(SpecimenConsentCopies, 'specimen_consent_copies_images')

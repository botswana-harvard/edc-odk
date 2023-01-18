from django.apps import apps as django_apps

from .reportmixin import ReportMixin
from ..models import *


class AdultReports(ReportMixin):
    app_config = django_apps.get_app_config('edc_odk')
    consent_model = app_config.adult_consent_model
    @property
    def missing_parental_consent(self):
        missing_parental_consent = []
        existing_parental_consent = []
        for subject_id in self.all_caregivers:
            try:
                obj = ParentalConsent.objects.get(subject_identifier=subject_id)
            except ParentalConsent.DoesNotExist:
                missing_parental_consent.append(subject_id)
            else:
                if obj.parental_consent_images.all().count() < 1:
                    missing_parental_consent.append(subject_id)
                else:
                    existing_parental_consent.append(subject_id)
        return {'missing': len(list(set(missing_parental_consent))),
                'existing': len(list(set(existing_parental_consent)))}

    @property
    def missing_omang_copies(self):
        missing_omang_copies = []
        existing_omang_copies = []
        for subject_id in self.all_caregivers:
            try:
                obj = OmangCopies.objects.get(subject_identifier=subject_id)
            except OmangCopies.DoesNotExist:
                missing_omang_copies.append(subject_id)
            else:
                if len(list(obj.national_id_images.all())) < 1:
                    missing_omang_copies.append(subject_id)
                else:
                    existing_omang_copies.append(subject_id)
        return {'missing': len(list(set(missing_omang_copies))),
                'existing': len(list(set(existing_omang_copies)))}

    @property
    def missing_adult_main_consent(self):
        missing_adult_main_consent = []
        existing_adult_main_consent = []
        for subject_id in self.all_caregivers:
            try:
                obj = AdultMainConsent.objects.get(subject_identifier=subject_id)
            except AdultMainConsent.DoesNotExist:
                missing_adult_main_consent.append(subject_id)
            else:
                if len(list(obj.adult_main_consent_images.all())) < 1:
                    missing_adult_main_consent.append(subject_id)
                else:
                    existing_adult_main_consent.append(subject_id)

        return {'missing': len(list(set(missing_adult_main_consent))),
                'existing': len(list(set(existing_adult_main_consent)))}

    @property
    def missing_note_to_files(self):
        missing_note_to_files = []
        existing_note_to_files = []
        for subject_id in self.all_caregivers:
            try:
                obj = NoteToFile.objects.get(subject_identifier=subject_id)
            except NoteToFile.DoesNotExist:
                missing_note_to_files.append(subject_id)
            else:
                if len(list(obj.note_to_file.all())) < 1:
                    missing_note_to_files.append(subject_id)
                else:
                    existing_note_to_files.append(subject_id)
        return {'missing': len(list(set(missing_note_to_files))),
                'existing': len(list(set(existing_note_to_files)))}

    @property
    def missing_lab_results_files(self):
        missing_lab_results_files = []
        existing_lab_results_files = []
        for subject_id in self.all_caregivers:
            try:
                obj = LabResultsFiles.objects.get(subject_identifier=subject_id)
            except LabResultsFiles.DoesNotExist:
                missing_lab_results_files.append(subject_id)
            else:
                if len(list(obj.lab_results.all())) < 1:
                    missing_lab_results_files.append(subject_id)
                else:
                    existing_lab_results_files.append(subject_id)
        return {'missing': len(list(set(missing_lab_results_files))),
                'existing': len(list(set(existing_lab_results_files)))}

    @property
    def missing_clinician_notes_archives(self):
        missing_clinician_notes_archives = []
        existing_clinician_notes_archives = []
        for subject_id in self.all_caregivers:
            try:
                obj = ClinicianNotesArchives.objects.get(subject_identifier=subject_id)
            except ClinicianNotesArchives.DoesNotExist:
                missing_clinician_notes_archives.append(subject_id)
            else:
                if len(list(obj.clinician_notes_archives.all())) < 1:
                    missing_clinician_notes_archives.append(subject_id)
                else:
                    existing_clinician_notes_archives.append(subject_id)
        return {'missing': len(list(set(missing_clinician_notes_archives))),
                'existing': len(list(set(existing_clinician_notes_archives)))}

    @property
    def missing_consent_copies(self):
        missing_consent_copies = []
        existing_consent_copies = []
        for subject_id in self.all_caregivers:
            try:
                obj = ConsentCopies.objects.get(subject_identifier=subject_id)
            except ConsentCopies.DoesNotExist:
                missing_consent_copies.append(subject_id)
            else:
                if len(list(obj.consent_images.all())) < 1:
                    missing_consent_copies.append(subject_id)
                else:
                    existing_consent_copies.append(subject_id)
        return {'missing': len(list(set(missing_consent_copies))),
                'existing': len(list(set(existing_consent_copies)))}

    @property
    def missing_specimen_consent_copies(self):
        missing_specimen_consent_copies = []
        existing_specimen_consent_copies = []
        for subject_id in self.all_caregivers:
            try:
                obj = SpecimenConsentCopies.objects.get(subject_identifier=subject_id)
            except SpecimenConsentCopies.DoesNotExist:
                missing_specimen_consent_copies.append(subject_id)
            else:
                if len(list(obj.specimen_consent_copies_images.all())) < 1:
                    missing_specimen_consent_copies.append(subject_id)
                else:
                    existing_specimen_consent_copies.append(subject_id)
        return {'missing': len(list(set(missing_specimen_consent_copies))),
                'existing': len(list(set(existing_specimen_consent_copies)))}

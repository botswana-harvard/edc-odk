from django.apps import apps as django_apps

from ..models import *


class MissingFiles:
    consent_model = 'flourish_caregiver.subjectconsent'

    @property
    def consent_cls(self):
        return django_apps.get_model(self.consent_model)

    @property
    def all_caregivers(self):
        return list(set(self.consent_cls.objects.all().values_list(
            'subject_identifier', flat=True).distinct()))

    @property
    def missing_adult_main_concent(self):
        pass

    @property
    def missing_parental_consent(self):
        missing_parental_consent = []
        for subject_id in self.all_caregivers:
            try:
                obj = ParentalConsent.objects.get(subject_identifier=subject_id)
            except ParentalConsent.DoesNotExist:
                missing_parental_consent.append(subject_id)
            else:
                if obj.parental_consent_images.all().count() < 1:
                    missing_parental_consent.append(subject_id)
        return len(list(set(missing_parental_consent)))

    @property
    def missing_omang_copies(self):
        missing_omang_copies = []
        for subject_id in self.all_caregivers:
            try:
                obj = OmangCopies.objects.get(subject_identifier=subject_id)
            except OmangCopies.DoesNotExist:
                missing_omang_copies.append(subject_id)
            else:
                if len(list(obj.national_id_images.all())) < 1:
                    missing_omang_copies.append(subject_id)
        return len(list(set(missing_omang_copies)))

    @property
    def missing_adult_main_consent(self):
        missing_adult_main_consent = []
        for subject_id in self.all_caregivers:
            try:
                obj = AdultMainConsent.objects.get(subject_identifier=subject_id)
            except AdultMainConsent.DoesNotExist:
                missing_adult_main_consent.append(subject_id)
            else:
                if len(list(obj.adult_main_consent_images.all())) < 1:
                    missing_adult_main_consent.append(subject_id)
        return len(list(set(missing_adult_main_consent)))

    @property
    def missing_note_to_files(self):
        missing_note_to_files = []
        for subject_id in self.all_caregivers:
            try:
                obj = NoteToFile.objects.get(subject_identifier=subject_id)
            except NoteToFile.DoesNotExist:
                missing_note_to_files.append(subject_id)
            else:
                if len(list(obj.note_to_file.all())) < 1:
                    missing_note_to_files.append(subject_id)
        return len(list(set(missing_note_to_files)))

    @property
    def missing_lab_results_files(self):
        missing_lab_results_files = []
        for subject_id in self.all_caregivers:
            try:
                obj = LabResultsFiles.objects.get(subject_identifier=subject_id)
            except LabResultsFiles.DoesNotExist:
                missing_lab_results_files.append(subject_id)
            else:
                if len(list(obj.lab_results.all())) < 1:
                    missing_lab_results_files.append(subject_id)
        return len(list(set(missing_lab_results_files)))



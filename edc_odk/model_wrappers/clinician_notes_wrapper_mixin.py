from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .clinician_notes_model_wrapper import ClinicianNotesModelWrapper


class ClinicianNotesModelWrapperMixin:

    clinician_notes_model_wrapper_cls = ClinicianNotesModelWrapper

    @property
    def clinician_notes_model_obj(self):
        """Returns a clinician notes model instance or None.
        """
        try:
            return self.clinician_notes_cls.objects.get(
                **self.clinician_notes_options)
        except ObjectDoesNotExist:
            return None

    @property
    def clinician_notes(self):
        """Returns a wrapped saved or unsaved clinician notes.
        """
        model_obj = self.clinician_notes_model_obj or self.clinician_notes_cls(
            **self.create_clinician_notes_options)
        if 'dashboard' in self.next_url_name:
            next_url_name = self.next_url_name
            return self.clinician_notes_model_wrapper_cls(
                model_obj=model_obj, next_url_name=next_url_name)
        return self.clinician_notes_model_wrapper_cls(model_obj=model_obj)

    @property
    def clinician_notes_cls(self):
        return django_apps.get_model('edc_odk.cliniciannotesarchives')

    @property
    def create_clinician_notes_options(self):
        """ Returns a dictionary of options to create a new
            unpersisted clinician notes model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def clinician_notes_options(self):
        """ Returns a dictionary of options to get an existing clinician notes
            model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

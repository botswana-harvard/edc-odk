from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .specimen_consent_model_wrapper import SpecimenConsentModelWrapper


class SpecimenConsentModelWrapperMixin:

    specimen_consent_copies_model_wrapper_cls = SpecimenConsentModelWrapper

    @property
    def specimen_consent_copies_model_obj(self):
        """Returns a omang copies model instance or None.
        """
        try:
            return self.specimen_consent_copies_cls.objects.get(
                **self.specimen_consent_copies_options)
        except ObjectDoesNotExist:
            return None

    @property
    def specimen_consent_copies(self):
        """Returns a wrapped saved or unsaved omang copies.
        """
        model_obj = self.specimen_consent_copies_model_obj or self.specimen_consent_copies_cls(
            **self.create_specimen_consent_copies_options)
        if 'dashboard' in self.next_url_name:
            next_url_name = self.next_url_name
            return self.specimen_consent_copies_model_wrapper_cls(
                model_obj=model_obj, next_url_name=next_url_name)
        return self.specimen_consent_copies_model_wrapper_cls(model_obj=model_obj)

    @property
    def specimen_consent_copies_cls(self):
        return django_apps.get_model('edc_odk.specimenconsentcopies')

    @property
    def create_specimen_consent_copies_options(self):
        """Returns a dictionary of options to create a new
        unpersisted omang copies model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def specimen_consent_copies_options(self):
        """Returns a dictionary of options to get an existing
        specimen consent copies model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

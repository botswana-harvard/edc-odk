from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .parental_consent_model_wrapper import ParentalConsentModelWrapper


class ParentalConsentModelWrapperMixin:
    parental_consent_model_wrapper_cls = ParentalConsentModelWrapper

    @property
    def parental_consent_model_obj(self):
        """Returns a parental consent model instance or None.
        """
        try:
            return self.parental_consent_cls.objects.get(
                **self.parental_consent_options)
        except ObjectDoesNotExist:
            return None

    @property
    def parental_consent(self):
        """Returns a wrapped saved or unsaved parental consent.
        """
        model_obj = self.parental_consent_model_obj or self.parental_consent_cls(
            **self.create_parental_consent_options)
        if 'dashboard' in self.next_url_name:
            next_url_name = self.next_url_name
            return self.parental_consent_model_wrapper_cls(
                model_obj=model_obj, next_url_name=next_url_name)
        return self.parental_consent_model_wrapper_cls(model_obj=model_obj)

    @property
    def parental_consent_cls(self):
        return django_apps.get_model('edc_odk.parentalconsent')

    @property
    def create_parental_consent_options(self):
        """ Returns a dictionary of options to create a new
            unpersisted parental consent model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def parental_consent_options(self):
        """ Returns a dictionary of options to get an existing parental consent
            model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .adult_main_consent_model_wrapper import AdultMainConsentModelWrapper


class AdultMainConsentModelWrapperMixin:
    adult_main_consent_model_wrapper_cls = AdultMainConsentModelWrapper

    @property
    def adult_main_consent_model_obj(self):
        """Returns a adult main consent model instance or None.
        """
        try:
            return self.adult_main_consent_cls.objects.get(
                **self.adult_main_consent_options)
        except ObjectDoesNotExist:
            return None

    @property
    def adult_main_consent(self):
        """Returns a wrapped saved or unsaved adult main consent.
        """
        model_obj = self.adult_main_consent_model_obj or self.adult_main_consent_cls(
            **self.create_adult_main_consent_options)
        if 'dashboard' in self.next_url_name:
            next_url_name = self.next_url_name
            return self.adult_main_consent_model_wrapper_cls(
                model_obj=model_obj, next_url_name=next_url_name)
        return self.adult_main_consent_model_wrapper_cls(model_obj=model_obj)

    @property
    def adult_main_consent_cls(self):
        return django_apps.get_model('edc_odk.adultmainconsent')

    @property
    def create_adult_main_consent_options(self):
        """ Returns a dictionary of options to create a new
            unpersisted adult main consent model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def adult_main_consent_options(self):
        """ Returns a dictionary of options to get an existing adult main consent
            model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

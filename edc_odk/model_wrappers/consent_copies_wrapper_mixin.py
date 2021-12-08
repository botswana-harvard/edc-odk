from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .consent_copies_model_wrapper import ConsentCopiesModelWrapper


class ConsentCopiesModelWrapperMixin:

    consent_copies_model_wrapper_cls = ConsentCopiesModelWrapper

    @property
    def consent_copies_model_obj(self):
        """Returns a consent copies model instance or None.
        """
        try:
            return self.consent_copies_cls.objects.get(
                **self.consent_copies_options)
        except ObjectDoesNotExist:
            return None

    @property
    def consent_copies(self):
        """Returns a wrapped saved or unsaved consent copies.
        """
        model_obj = self.consent_copies_model_obj or self.consent_copies_cls(
            **self.create_consent_copies_options)
        return self.consent_copies_model_wrapper_cls(model_obj=model_obj)

    @property
    def consent_copies_cls(self):
        return django_apps.get_model('edc_odk.consentcopies')

    @property
    def create_consent_copies_options(self):
        """Returns a dictionary of options to create a new
        unpersisted consent copies model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def consent_copies_options(self):
        """Returns a dictionary of options to get an existing
        consent copies model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

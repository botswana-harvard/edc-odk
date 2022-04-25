from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .birth_certificate_model_wrapper import BirthCertificateModelWrapper


class BirthCertificateModelWrapperMixin:
    birth_certificate_model_wrapper_cls = BirthCertificateModelWrapper

    @property
    def birth_certificate_model_obj(self):
        """Returns a birth certificate model instance or None.
        """
        try:
            return self.birth_certificate_cls.objects.get(
                **self.birth_certificate_options)
        except ObjectDoesNotExist:
            return None

    @property
    def birth_certificate(self):
        """Returns a wrapped saved or unsaved birth certificate.
        """
        model_obj = self.birth_certificate_model_obj or self.birth_certificate_cls(
            **self.create_birth_certificate_options)
        if 'dashboard' in self.next_url_name:
            next_url_name = self.next_url_name
            return self.birth_certificate_model_wrapper_cls(
                model_obj=model_obj, next_url_name=next_url_name)
        return self.birth_certificate_model_wrapper_cls(model_obj=model_obj)

    @property
    def birth_certificate_cls(self):
        return django_apps.get_model('edc_odk.birthcertificate')

    @property
    def create_birth_certificate_options(self):
        """ Returns a dictionary of options to create a new
            unpersisted birth certificate model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def birth_certificate_options(self):
        """ Returns a dictionary of options to get an existing birth certificate
            model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

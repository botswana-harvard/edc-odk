from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_model_wrapper import ModelWrapper


class ConsentCopiesModelWrapper(ModelWrapper):

    model = 'edc_odk.consentcopies'
    consent_image_model = 'edc_odk.consentimage'
    specimen_consent_image_model = 'edc_odk.specimenconsentimage'
    nation_id_image_model = 'edc_odk.nationalidentityimage'

    next_url_name = settings.DASHBOARD_URL_NAMES.get('odk_listboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier']

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
        """Returns a wrapped saved or unsaved subject screening.
        """
        model_obj = self.consent_copies_model_obj or self.consent_copies_cls(
            **self.create_consent_copies_options)
        return ConsentCopiesModelWrapper(model_obj=model_obj)

    @property
    def consent_copies_cls(self):
        return django_apps.get_model('edc_odk.consentcopies')

    @property
    def create_consent_copies_options(self):
        """Returns a dictionary of options to create an instance of
        consent copies model.
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

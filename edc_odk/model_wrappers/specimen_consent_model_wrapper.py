from django.conf import settings

from edc_model_wrapper import ModelWrapper


class SpecimenConsentModelWrapper(ModelWrapper):

    model = 'edc_odk.specimenconsentcopies'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'odk_listboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier']

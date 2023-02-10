from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'edc_odk'
    verbose_name = "EDC ODK"
    admin_site_name = 'edc_odk_admin'
    adult_child_study=False
    adult_consent_model=''
    child_assent_model=''


clinician_notes_models = {'default': 'cliniciannotes'}

clinician_notes_form_ids = dict()

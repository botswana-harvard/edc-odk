from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'edc_odk'
    verbose_name = "EDC ODK"
    admin_site_name = 'edc_odk_admin'


clinician_notes_models = {'default': 'cliniciannotes'}

clinician_notes_form_ids = dict()

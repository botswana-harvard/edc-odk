from django.apps import apps as django_apps


class ReportMixin:
    app_config = django_apps.get_app_config('edc_odk')
    consent_model = app_config.adult_consent_model

    @property
    def consent_cls(self):
        return django_apps.get_model(self.consent_model)

    @property
    def all_caregivers(self):
        return list(set(self.consent_cls.objects.all().values_list(
            'subject_identifier', flat=True).distinct()))

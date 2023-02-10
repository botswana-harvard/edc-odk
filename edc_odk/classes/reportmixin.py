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

    def check_missing(self, model, attr):
        missing = []
        existing = []
        for subject_id in self.all_caregivers:
            try:
                obj = model.objects.get(subject_identifier=subject_id)
            except model.DoesNotExist:
                missing.append(subject_id)
            else:
                if len(list(getattr(obj, attr).all())) < 1:
                    missing.append(subject_id)
                else:
                    existing.append(subject_id)
        return {'missing': len(list(set(missing))),
                'existing': len(list(set(existing)))}

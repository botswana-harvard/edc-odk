from django.apps import apps as django_apps

from .reportmixin import ReportMixin
from ..models import Assent, ContinuedParticipation, BirthCertificate


class ChildrenReports(ReportMixin):
    app_config = django_apps.get_app_config('edc_odk')
    consent_model = app_config.child_assent_model

    @property
    def missing_assent(self):
        return self.check_missing(Assent, 'assent_images')

    @property
    def missing_continued_participation(self):
        return self.check_missing(ContinuedParticipation,
                                  'continued_participation_images')

    @property
    def missing_birth_certificate(self):
        return self.check_missing(BirthCertificate, 'birth_certificate_images')

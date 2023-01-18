from django.apps import apps as django_apps

from .reportmixin import ReportMixin
from ..models import Assent, ContinuedParticipation, BirthCertificate


class ChildrenReports(ReportMixin):
    app_config = django_apps.get_app_config('edc_odk')
    consent_model = app_config.child_assent_model

    @property
    def missing_assent(self):
        missing_assent = []
        existing_assent = []
        for subject_id in self.all_caregivers:
            try:
                obj = Assent.objects.get(subject_identifier=subject_id)
            except Assent.DoesNotExist:
                missing_assent.append(subject_id)
            else:
                if len(list(obj.assent_images.all())) < 1:
                    missing_assent.append(subject_id)
                else:
                    existing_assent.append(subject_id)
        return {'missing': len(list(set(missing_assent))),
                'existing': len(list(set(existing_assent)))}

    @property
    def missing_continued_participation(self):
        missing_continued_participation = []
        existing_continued_participation = []
        for subject_id in self.all_caregivers:
            try:
                obj = ContinuedParticipation.objects.get(subject_identifier=subject_id)
            except ContinuedParticipation.DoesNotExist:
                missing_continued_participation.append(subject_id)
            else:
                if len(list(obj.continued_participation_images.all())) < 1:
                    missing_continued_participation.append(subject_id)
                else:
                    existing_continued_participation.append(subject_id)
        return {'missing': len(list(set(missing_continued_participation))),
                'existing': len(list(set(existing_continued_participation)))}

    @property
    def missing_birth_certificate(self):
        missing_birth_certificate = []
        existing_birth_certificate = []
        for subject_id in self.all_caregivers:
            try:
                obj = BirthCertificate.objects.get(subject_identifier=subject_id)
            except BirthCertificate.DoesNotExist:
                missing_birth_certificate.append(subject_id)
            else:
                if len(list(obj.birth_certificate_images.all())) < 1:
                    missing_birth_certificate.append(subject_id)
                else:
                    existing_birth_certificate.append(subject_id)
        return {'missing': len(list(set(missing_birth_certificate))),
                'existing': len(list(set(existing_birth_certificate)))}

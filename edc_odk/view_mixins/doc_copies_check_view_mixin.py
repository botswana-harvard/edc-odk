from django.apps import apps as django_apps
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.views.generic.base import ContextMixin


class DocCopiesCheckViewMixin(ContextMixin):

    omang_copies_cls = django_apps.get_model('edc_odk.omangcopies')
    consent_copies_cls = django_apps.get_model('edc_odk.consentcopies')
    specimen_copies_cls = django_apps.get_model('edc_odk.specimenconsentcopies')

    def get_omang_copies_or_message(self):
        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            self.omang_copies_cls.objects.get(
                subject_identifier=subject_identifier)
        except self.omang_copies_cls.DoesNotExist:
            form = self.omang_copies_cls._meta.verbose_name
            msg = mark_safe(
                f'{form} missing for this subject, Please add copies.')
            messages.add_message(self.request, messages.WARNING, msg)

    def get_consent_copies_or_message(self):
        subject_identifier = self.kwargs.get('subject_identifier')

        consent_copies = self.consent_copies_cls.objects.filter(
                subject_identifier=subject_identifier)
        if not consent_copies:
            form = self.consent_copies_cls._meta.verbose_name
            msg = mark_safe(
                f'{form} missing for this subject, Please add copies.')
            messages.add_message(self.request, messages.WARNING, msg)

    def get_specimen_consent_copies_or_message(self):
        subject_identifier = self.kwargs.get('subject_identifier')

        specimen_consent = self.specimen_copies_cls.objects.filter(
                subject_identifier=subject_identifier)
        if not specimen_consent:
            form = self.specimen_copies_cls._meta.verbose_name
            msg = mark_safe(
                f'{form} missing for this subject, Please add copies.')
            messages.add_message(self.request, messages.WARNING, msg)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.get_omang_copies_or_message()
        self.get_consent_copies_or_message()
        self.get_specimen_consent_copies_or_message()

        return context

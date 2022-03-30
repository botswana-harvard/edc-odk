from django.db import models
from django.utils.html import mark_safe
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin


class SpecimenConsentCopies(
        UniqueSubjectIdentifierFieldMixin, SiteModelMixin, BaseUuidModel):

    @property
    def related_objects(self):
        return getattr(self, 'specimen_consent_images')

    class Meta:
        app_label = 'edc_odk'
        verbose_name = 'Specimen Consent Copies'
        verbose_name_plural = 'Specimen Consent Copies'


class SpecimenConsentImage(BaseUuidModel):

    consent_copies = models.ForeignKey(
        SpecimenConsentCopies,
        on_delete=models.PROTECT,
        related_name='specimen_consent_images')

    image = models.FileField(upload_to='specimen_consent/')

    user_uploaded = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='user uploaded',)

    datetime_captured = models.DateTimeField(
        default=get_utcnow)

    def specimen_consent_image(self):
            return mark_safe(
                '<embed src="%(url)s" style="border:none" height="100" width="150"'
                'title="speciment consent"></embed>' % {'url': self.image.url})

    specimen_consent_image.short_description = 'Specimen Consent Image'
    specimen_consent_image.allow_tags = True

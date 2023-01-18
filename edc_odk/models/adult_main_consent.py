from django.db import models
from django.utils.html import mark_safe
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_consent.field_mixins import VerificationFieldsMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin


class AdultMainConsent(VerificationFieldsMixin, NonUniqueSubjectIdentifierModelMixin,
                       SiteModelMixin, BaseUuidModel):
    version = models.CharField(
        verbose_name='Consent version',
        max_length=10,
        help_text='See \'Consent Type\' for consent versions by period.')

    @property
    def related_objects(self):
        return getattr(self, 'adult_main_consent_images')


    class Meta:
        app_label = 'edc_odk'
        verbose_name = 'Adult Main Consent'
        verbose_name_plural = 'Adult Main Consent'
        unique_together = ('subject_identifier', 'version')


class AdultMainConsentImage(BaseUuidModel):
    adult_main_consent = models.ForeignKey(
        AdultMainConsent,
        on_delete=models.PROTECT,
        related_name='adult_main_consent_images', )

    image = models.FileField(upload_to='adult_main_consent_images/')

    user_uploaded = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='user uploaded', )

    datetime_captured = models.DateTimeField(
        default=get_utcnow)

    def adult_consent_image(self):
        return mark_safe(
            '<embed src="%(url)s" style="border:none" height="100" width="150"'
            'title="clinician notes"></embed>' % {'url': self.image.url})

    adult_consent_image.short_description = 'Adult Main Consent Image'
    adult_consent_image.allow_tags = True

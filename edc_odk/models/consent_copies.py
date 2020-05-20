from django.db import models
from django.utils.html import mark_safe
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin


class ConsentCopies(
        NonUniqueSubjectIdentifierModelMixin, SiteModelMixin, BaseUuidModel):

    version = models.CharField(
        verbose_name='Consent version',
        max_length=10,
        help_text='See \'Consent Type\' for consent versions by period.',
        editable=False)

    class Meta:
        app_label = 'edc_odk'
        verbose_name = 'Consent Copies'
        verbose_name_plural = 'Consent Copies'
        unique_together = ('subject_identifier', 'version')


class ConsentImage(BaseUuidModel):

    consent_copies = models.ForeignKey(
        ConsentCopies,
        on_delete=models.PROTECT,
        related_name='consent_images',)
    image = models.ImageField(upload_to='media/')
    user_uploaded = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='user uploaded',)
    datetime_captured = models.DateTimeField(
        default=get_utcnow)

    def consent_image(self):
            return mark_safe(
                '<a href="%(url)s">'
                '<img src="%(url)s" style="padding-right:150px" width="150" height="100" />'
                '</a>' % {'url': self.image.url})

    consent_image.short_description = 'Consent Image'
    consent_image.allow_tags = True


class SpecimenConsentImage(BaseUuidModel):

    consent_copies = models.ForeignKey(
        ConsentCopies,
        on_delete=models.PROTECT,
        related_name='specimen_consent_images',)
    image = models.ImageField(upload_to='media/')
    user_uploaded = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='user uploaded',)
    datetime_captured = models.DateTimeField(
        default=get_utcnow)

    def specimen_consent_image(self):
            return mark_safe(
                '<a href="%(url)s">'
                '<img src="%(url)s" style="padding-right:150px" width="150" height="100" />'
                '</a>' % {'url': self.image.url})

    specimen_consent_image.short_description = 'Specimen Consent Image'
    specimen_consent_image.allow_tags = True

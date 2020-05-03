from django.db import models
from django.utils.html import mark_safe
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.model_mixins import BaseUuidModel
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin


class ConsentCopies(
        UniqueSubjectIdentifierFieldMixin, SiteModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'edc_odk'
        verbose_name = 'Consent Copies'
        verbose_name_plural = 'Consent Copies'


class ConsentImage(BaseUuidModel):

    consent_copies = models.ForeignKey(
        ConsentCopies,
        on_delete=models.PROTECT,
        related_name='consent_images',)
    image = models.ImageField(upload_to='media/')

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

    def specimen_consent_image(self):
            return mark_safe(
                '<a href="%(url)s">'
                '<img src="%(url)s" style="padding-right:150px" width="150" height="100" />'
                '</a>' % {'url': self.image.url})

    specimen_consent_image.short_description = 'Specimen Consent Image'
    specimen_consent_image.allow_tags = True


class NationalIdentityImage(BaseUuidModel):

    consent_copies = models.ForeignKey(
        ConsentCopies,
        on_delete=models.PROTECT,
        related_name='national_id_images',)
    image = models.ImageField(upload_to='media/')

    def national_identity_image(self):
            return mark_safe(
                '<a href="%(url)s">'
                '<img src="%(url)s" style="padding-right:150px" width="150" height="100" />'
                '</a>' % {'url': self.image.url})

    national_identity_image.short_description = 'National Identity Image'
    national_identity_image.allow_tags = True

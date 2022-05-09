from django.db import models
from django.utils.html import mark_safe
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin


class BirthCertificate(
        NonUniqueSubjectIdentifierModelMixin, SiteModelMixin, BaseUuidModel):

    @property
    def related_objects(self):
        return getattr(self, 'birth_certificate_images')

    class Meta:
        app_label = 'edc_odk'
        verbose_name = 'Birth Certificate'
        verbose_name_plural = 'Birth Certificates'


class BirthCertificateImage(BaseUuidModel):

    birth_certificate = models.ForeignKey(
        BirthCertificate,
        on_delete=models.PROTECT,
        related_name='birth_certificate_images',)

    image = models.FileField(upload_to='birth_certificate_images/')

    user_uploaded = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='user uploaded',)

    datetime_captured = models.DateTimeField(
        default=get_utcnow)

    def birth_certificate_image(self):
        return mark_safe(
            '<embed src="%(url)s" style="border:none" height="100" width="150"'
            'title="consent copy"></embed>' % {'url': self.image.url})

    birth_certificate_image.short_description = 'Birth Certificate Image'
    birth_certificate_image.allow_tags = True

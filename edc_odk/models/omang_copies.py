from django.db import models
from django.utils.html import mark_safe
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_consent.field_mixins import VerificationFieldsMixin

class OmangCopies(VerificationFieldsMixin, UniqueSubjectIdentifierFieldMixin,
                  SiteModelMixin, BaseUuidModel):

    @property
    def related_objects(self):
        return getattr(self, 'national_id_images')


    class Meta:
        app_label = 'edc_odk'
        verbose_name = 'Omang Copies'
        verbose_name_plural = 'Omang Copies'


class NationalIdentityImage(BaseUuidModel):
    omang_copies = models.ForeignKey(
        OmangCopies,
        on_delete=models.PROTECT,
        related_name='national_id_images', )

    image = models.FileField(upload_to='omang_copies/')

    user_uploaded = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='user uploaded', )

    datetime_captured = models.DateTimeField(
        default=get_utcnow)

    def national_identity_image(self):
        return mark_safe(
            '<embed src="%(url)s" style="border:none" height="100" width="150"'
            'title="omang copy"></embed>' % {'url': self.image.url})

    national_identity_image.short_description = 'National Identity Image'
    national_identity_image.allow_tags = True

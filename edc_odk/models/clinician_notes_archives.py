from django.db import models
from django.utils.html import mark_safe
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin


class ClinicianNotesArchives(
        UniqueSubjectIdentifierFieldMixin, SiteModelMixin, BaseUuidModel):

    @property
    def related_objects(self):
        return getattr(self, 'clinician_notes_archives')

    class Meta:
        app_label = 'edc_odk'
        verbose_name = 'Clinician Notes Archives'
        verbose_name_plural = 'Clinician Notes Archives'


class ClinicianNotesImageArchive(BaseUuidModel):

    clinician_notes = models.ForeignKey(
        ClinicianNotesArchives,
        on_delete=models.PROTECT,
        related_name='clinician_notes_archives',)

    image = models.FileField(upload_to='clinician_notes_archives/')

    user_uploaded = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='user uploaded',)

    datetime_captured = models.DateTimeField(
        default=get_utcnow)

    def clinician_notes_image(self):
        return mark_safe(
            '<embed src="%(url)s" style="border:none" height="100" width="150"'
            'title="clinician notes"></embed>' % {'url': self.image.url})

    clinician_notes_image.short_description = 'Clinician Notes Image'
    clinician_notes_image.allow_tags = True

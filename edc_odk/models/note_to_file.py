from django.db import models
from django.utils.html import mark_safe
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin


class NoteToFile(UniqueSubjectIdentifierFieldMixin, SiteModelMixin, BaseUuidModel):

    @property
    def related_objects(self):
        return getattr(self, 'note_to_file')

    class Meta:
        app_label = 'edc_odk'
        verbose_name = 'Note to file'
        verbose_name_plural = 'Notes to file'


class NoteToFileDocs(BaseUuidModel):

    notes_to_file = models.ForeignKey(
        NoteToFile,
        on_delete=models.PROTECT,
        related_name='note_to_file')

    def upload_to_path(instance, filename):
        today = get_utcnow().date().strftime('%Y/%m/%d')
        if filename:
            return f'notes_to_file/{today}/{filename}'
        return f'notes_to_file/{today}/'

    image = models.FileField(upload_to='notes_to_file/')

    user_uploaded = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='user uploaded',)

    datetime_captured = models.DateTimeField(
        default=get_utcnow)

    def ntf_document(self):
            return mark_safe(
                '<embed src="%(url)s" style="border:none" height="100" width="150"'
                'title="note to file"></embed>' % {'url': self.image.url})

    ntf_document.short_description = 'Preview'
    ntf_document.allow_tags = True


from django.db import models
from django.utils.html import mark_safe
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow


class NoteToFile(SiteModelMixin, BaseUuidModel):

    identifier = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = get_utcnow().strftime('%Y%m%d%H%M%S')
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'edc_odk'
        verbose_name = 'Note to file'
        verbose_name_plural = 'Notes to file'


def upload_to_path(instance, filename):
    today = get_utcnow().date().strftime('%Y/%m/%d')
    if filename:
        return f'notes_to_file/{today}/{filename}'
    return f'notes_to_file/{today}/'


class NoteToFileDocs(BaseUuidModel):

    notes_to_file = models.ForeignKey(
        NoteToFile,
        on_delete=models.PROTECT,
        related_name='notes_to_file',)

    image = models.FileField(upload_to=upload_to_path)

    user_uploaded = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='user uploaded',)

    datetime_captured = models.DateTimeField(
        default=get_utcnow)

    def ntf_document(self):
            return mark_safe(
                '<iframe src="%(url)s" style="border:none" height="120" width="120"'
                'title="note to file" scrolling="yes"></iframe>' % {'url': self.image.url})

    ntf_document.short_description = 'Preview'
    ntf_document.allow_tags = True


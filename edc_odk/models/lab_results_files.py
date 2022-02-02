from django.db import models
from django.utils.html import mark_safe
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin


class LabResultsFiles(
        UniqueSubjectIdentifierFieldMixin, SiteModelMixin, BaseUuidModel):

    @property
    def related_objects(self):
        return getattr(self, 'lab_results')

    class Meta:
        app_label = 'edc_odk'
        verbose_name = 'Lab Results Files'
        verbose_name_plural = 'Lab Results Files'


class LabResultsFile(BaseUuidModel):

    lab_results = models.ForeignKey(
        LabResultsFiles,
        on_delete=models.PROTECT,
        related_name='lab_results',)

    image = models.FileField(upload_to='lab_results/')

    user_uploaded = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='user uploaded',)

    datetime_captured = models.DateTimeField(
        default=get_utcnow)

    def lab_results_preview(self):
        return mark_safe(
            '<embed src="%(url)s" style="border:none" height="100" width="150"'
            'title="lab results"></embed>' % {'url': self.image.url})

    lab_results_preview.short_description = 'Preview'
    lab_results_preview.allow_tags = True

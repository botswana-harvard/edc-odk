from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from .stampimage_action_mixin import StampImageActionMixin

from ..admin_site import edc_odk_admin
from ..forms import LabResultsFilesForm, LabResultsFileForm
from ..models import LabResultsFiles, LabResultsFile
from .modeladmin_mixins import ModelAdminMixin


class LabResultsFileInline(TabularInlineMixin, admin.TabularInline):

    model = LabResultsFile
    form = LabResultsFileForm
    extra = 0
    min_num = 1

    fields = ('lab_results_preview', 'image', 'user_uploaded', 'datetime_captured',
              'modified', 'hostname_created',)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = (
            'lab_results_preview', 'datetime_captured', 'user_uploaded') + fields

        return fields


@admin.register(LabResultsFiles, site=edc_odk_admin)
class LabResultsFilesAdmin(
        ModelAdminMixin, StampImageActionMixin, admin.ModelAdmin):

    form = LabResultsFilesForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
            ]}
         ), )

    list_display = ('subject_identifier', 'created', )

    inlines = [LabResultsFileInline]

    search_fields = ('subject_identifier',)

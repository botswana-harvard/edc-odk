from django.contrib import admin
from edc_model_admin import TabularInlineMixin

from ..admin_site import edc_odk_admin
from ..forms import ClinicianNotesImageArchiveForm, ClinicianNotesArchivesForm
from ..models import ClinicianNotesArchives, ClinicianNotesImageArchive
from .modeladmin_mixins import ModelAdminMixin


class ClinicianNotesImageInline(TabularInlineMixin, admin.TabularInline):

    model = ClinicianNotesImageArchive
    form = ClinicianNotesImageArchiveForm
    extra = 0
    min_num = 1

    fields = ('clinician_notes_image', 'image', 'user_uploaded', 'datetime_captured',
              'modified', 'hostname_created',)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = (
            'clinician_notes_image', 'datetime_captured', 'user_uploaded') + fields

        return fields


@admin.register(ClinicianNotesArchives, site=edc_odk_admin)
class ClinicianNotesArchivesAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ClinicianNotesArchivesForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
            ]}
         ),)

    list_display = ('subject_identifier', 'created', 'verified_by', 'is_verified',)

    inlines = [ClinicianNotesImageInline]

    search_fields = ('subject_identifier',)

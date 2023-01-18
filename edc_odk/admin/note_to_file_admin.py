from django.contrib import admin
from edc_model_admin import TabularInlineMixin, audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import edc_odk_admin
from ..models import NoteToFile
from ..models import NoteToFileDocs
from ..forms import NoteToFileForm
from ..forms import NoteToFileDocsForm


class NoteToFileDocsInline(TabularInlineMixin, admin.TabularInline):
    model = NoteToFileDocs
    form = NoteToFileDocsForm
    extra = 0
    min_num = 1

    fields = ('ntf_document', 'image', 'user_uploaded', 'datetime_captured',
              'modified', 'hostname_created',)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = ('ntf_document', 'datetime_captured', 'user_uploaded') + fields

        return fields


@admin.register(NoteToFile, site=edc_odk_admin)
class NoteToFileAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = NoteToFileForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                ]
            }), audit_fieldset_tuple, )

    inlines = [NoteToFileDocsInline]

    list_display = ('subject_identifier', 'created', 'verified_by', 'is_verified',)

    search_fields = ('subject_identifier', )

from django.contrib import admin
from edc_model_admin import TabularInlineMixin

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import edc_odk_admin
from ..models import OmangCopies
from ..models import NationalIdentityImage
from ..forms import OmangCopiesForm
from ..forms import NationalIdentityImageForm


class NationalIdentityImageInline(TabularInlineMixin, admin.TabularInline):
    model = NationalIdentityImage
    form = NationalIdentityImageForm
    extra = 0

    fields = ('national_identity_image', 'image', 'user_uploaded', 'datetime_captured',
              'modified', 'hostname_created',)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = (
            'national_identity_image', 'datetime_captured', 'user_uploaded') + fields

        return fields


@admin.register(OmangCopies, site=edc_odk_admin)
class OmangCopiesAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = OmangCopiesForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier', ]}),
        )

    list_display = ('subject_identifier', 'created', )

    inlines = [NationalIdentityImageInline]

    search_fields = ('subject_identifier', )

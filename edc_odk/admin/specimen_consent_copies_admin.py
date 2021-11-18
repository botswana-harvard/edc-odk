from django.contrib import admin
from edc_model_admin import TabularInlineMixin

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import edc_odk_admin
from ..models import SpecimenConsentCopies
from ..models import SpecimenConsentImage
from ..forms import SpecimenConsentCopiesForm
from ..forms import SpecimenConsentImageForm


class SpecimenConsentImageInline(TabularInlineMixin, admin.TabularInline):
    model = SpecimenConsentImage
    form = SpecimenConsentImageForm
    extra = 0

    fields = ('specimen_consent_image', 'user_uploaded', 'datetime_captured',
              'modified', 'hostname_created',)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = (
            'specimen_consent_image', 'datetime_captured', 'user_uploaded') + fields

        return fields


@admin.register(SpecimenConsentCopies, site=edc_odk_admin)
class SpecimenConsentCopiesAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = SpecimenConsentCopiesForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier', ]}),
        )

    list_display = ('subject_identifier', 'created', )

    inlines = [SpecimenConsentImageInline]

    search_fields = ('subject_identifier', )

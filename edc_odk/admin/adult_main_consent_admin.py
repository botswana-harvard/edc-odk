from django.contrib import admin
from edc_model_admin import TabularInlineMixin

from ..admin_site import edc_odk_admin
from ..forms import AdultMainConsentForm, AdultMainConsentImageForm
from ..models import AdultMainConsent, AdultMainConsentImage
from .modeladmin_mixins import ModelAdminMixin


class AdultMainConsentImageInline(TabularInlineMixin, admin.TabularInline):

    model = AdultMainConsentImage
    form = AdultMainConsentImageForm
    extra = 0
    min_num = 1

    fields = ('adult_consent_image', 'adult_main_consent', 'image', 'user_uploaded',
            'datetime_captured', 'modified', 'hostname_created',)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = (
            'adult_main_consent', 'adult_consent_image', 'datetime_captured', 'user_uploaded') + fields

        return fields


@admin.register(AdultMainConsent, site=edc_odk_admin)
class AdultMainConsentAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = AdultMainConsentForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
            ]}
        ),)


    list_display = ('subject_identifier', 'created', 'verified_by', 'is_verified',)

    inlines = [AdultMainConsentImageInline]

    search_fields = ('subject_identifier',)

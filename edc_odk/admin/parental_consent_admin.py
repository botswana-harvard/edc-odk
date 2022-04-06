from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from .stampimage_action_mixin import StampImageActionMixin

from ..admin_site import edc_odk_admin
from ..forms import ParentalConsentForm, ParentalConsentImageForm
from ..models import ParentalConsent, ParentalConsentImage
from .modeladmin_mixins import ModelAdminMixin


class ParentalConsentImageInline(TabularInlineMixin, admin.TabularInline):

    model = ParentalConsentImage
    form = ParentalConsentImageForm
    extra = 0
    min_num = 1

    fields = ('parental_consent_image', 'parental_consent', 'image',
            'user_uploaded', 'datetime_captured', 'modified',
            'hostname_created',)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = (
            'parental_consent_image', 'parental_consent', 'datetime_captured',
            'user_uploaded') + fields

        return fields


@admin.register(ParentalConsent, site=edc_odk_admin)
class ParentalConsentAdmin(ModelAdminMixin, StampImageActionMixin, admin.ModelAdmin):

    form = ParentalConsentForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
            ]}
        ),)

    list_display = ('subject_identifier', 'created', )

    inlines = [ParentalConsentImageInline]

    search_fields = ('subject_identifier',)

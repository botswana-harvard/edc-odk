from django.contrib import admin
from edc_model_admin import TabularInlineMixin

from ..admin_site import edc_odk_admin
from ..forms import BirthCertificateForm, BirthCertificateImageForm
from ..models import BirthCertificate, BirthCertificateImage
from .modeladmin_mixins import ModelAdminMixin

class BirthCertificateImageInline(TabularInlineMixin, admin.TabularInline):

    model = BirthCertificateImage
    form = BirthCertificateImageForm
    extra = 0
    min_num = 1

    fields = ('birth_certificate_image', 'birth_certificate', 'image', 'user_uploaded',
            'datetime_captured', 'modified', 'hostname_created',)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = (
            'birth_certificate_image', 'birth_certificate', 'datetime_captured', 'user_uploaded') + fields

        return fields


@admin.register(BirthCertificate, site=edc_odk_admin)
class BirthCertificateAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = BirthCertificateForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
            ]}
        ),)

    list_display = ('subject_identifier', 'created', 'verified_by', 'is_verified',)

    inlines = [BirthCertificateImageInline]

    search_fields = ('subject_identifier',)

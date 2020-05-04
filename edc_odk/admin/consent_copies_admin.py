from django.contrib import admin
from edc_model_admin import TabularInlineMixin, audit_fields

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import edc_odk_admin
from ..models import ConsentCopies
from ..models import (
    ConsentImage, SpecimenConsentImage, NationalIdentityImage)
from ..forms import ConsentCopiesForm
from ..forms import (
    ConsentImageForm, SpecimenConsentImageForm, NationalIdentityImageForm)


class ConsentImageInline(TabularInlineMixin, admin.TabularInline):
    model = ConsentImage
    form = ConsentImageForm
    extra = 0

    fields = ('consent_image', audit_fields)

    readonly_fields = ('consent_image',)


class SpecimenConsentImageInline(TabularInlineMixin, admin.TabularInline):
    model = SpecimenConsentImage
    form = SpecimenConsentImageForm
    extra = 0

    fields = ('specimen_consent_image', audit_fields)

    readonly_fields = ('specimen_consent_image',)


class NationalIdentityImageInline(TabularInlineMixin, admin.TabularInline):
    model = NationalIdentityImage
    form = NationalIdentityImageForm
    extra = 0

    fields = ('national_identity_image', audit_fields)

    readonly_fields = ('national_identity_image',)


@admin.register(ConsentCopies, site=edc_odk_admin)
class ConsentCopiesAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ConsentCopiesForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier', ]}),
        )

    list_display = ('subject_identifier', 'version', 'created', )

    inlines = [ConsentImageInline, SpecimenConsentImageInline,
               NationalIdentityImageInline]

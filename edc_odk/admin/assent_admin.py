from django.contrib import admin
from edc_model_admin import TabularInlineMixin

from ..admin_site import edc_odk_admin
from ..forms import AssentForm, AssentImageForm
from ..models import Assent, AssentImage
from .modeladmin_mixins import ModelAdminMixin
from .stampimage_action_mixin import StampImageActionMixin


class AssentImageInline(TabularInlineMixin, admin.TabularInline):

    model = AssentImage
    form = AssentImageForm
    extra = 0
    min_num = 1

    fields = ('assent_image', 'assent', 'image', 'user_uploaded',
              'datetime_captured', 'modified', 'hostname_created',)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = (
            'assent_image', 'assent', 'datetime_captured', 'user_uploaded') + fields

        return fields


@admin.register(Assent, site=edc_odk_admin)
class AssentAdmin(ModelAdminMixin, StampImageActionMixin, admin.ModelAdmin):

    form = AssentForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
            ]}),
    )

    list_display = ('subject_identifier', 'created',)

    inlines = [AssentImageInline]

    search_fields = ('subject_identifier',)

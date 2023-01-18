from django.contrib import admin
from edc_model_admin import TabularInlineMixin


from ..admin_site import edc_odk_admin
from ..forms import ContinuedParticipationForm, ContinuedParticipationImageForm
from ..models import ContinuedParticipation, ContinuedParticipationImage
from .modeladmin_mixins import ModelAdminMixin


class ContinuedParticipationImageInline(TabularInlineMixin, admin.TabularInline):

    model = ContinuedParticipationImage
    form = ContinuedParticipationImageForm
    extra = 0
    min_num = 1

    fields = ('continued_participation_image', 'continued_participation',
            'image', 'user_uploaded', 'datetime_captured', 'modified',
            'hostname_created',)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = (
            'continued_participation_image', 'continued_participation',
            'datetime_captured', 'user_uploaded') + fields

        return fields


@admin.register(ContinuedParticipation, site=edc_odk_admin)
class ContinuedParticipationAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ContinuedParticipationForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
            ]}
        ),)

    list_display = ('subject_identifier', 'created', 'verified_by', 'is_verified',)

    inlines = [ContinuedParticipationImageInline]

    search_fields = ('subject_identifier',)

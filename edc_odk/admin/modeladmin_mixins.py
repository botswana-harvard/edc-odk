from django.conf import settings
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_metadata import NextFormGetter
from edc_model_admin import (
    ModelAdminAuditFieldsMixin, ModelAdminFormAutoNumberMixin,
    ModelAdminFormInstructionsMixin, ModelAdminInstitutionMixin,
    ModelAdminNextUrlRedirectMixin, ModelAdminReadOnlyMixin,
    ModelAdminRedirectOnDeleteMixin, ModelAdminNextUrlRedirectError)

from .stampimage_action_mixin import StampImageActionMixin


class ModelAdminMixin(
        ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
        ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
        ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
        ModelAdminInstitutionMixin, ModelAdminRedirectOnDeleteMixin,
        ModelAdminSiteMixin, StampImageActionMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'
    next_form_getter_cls = NextFormGetter

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)

        if request.GET.dict().get('next'):
            url_name = request.GET.dict().get('next').split(',')[0]
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}

            url_name = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')
            options['subject_identifier'] = request.GET.get('subject_identifier')
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url

from django.conf import settings
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import ListboardView as BaseListboardView
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_navbar import NavbarViewMixin

from edc_odk.model_wrappers import ConsentCopiesModelWrapper

from ....classes import PullODKData, ODKCentralPullData


class ListboardView(EdcBaseViewMixin, NavbarViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin,
                    BaseListboardView):

    listboard_template = 'odk_listboard_template'
    listboard_url = 'odk_listboard_url'
    listboard_panel_style = 'success'
    listboard_fa_icon = "fa fa-file-image"

    model = 'edc_odk.consentcopies'
    model_wrapper_cls = ConsentCopiesModelWrapper
    navbar_name = 'edc_odk_forms'
    navbar_selected_item = 'edc_odk_forms'
    search_form_url = 'odk_listboard_url'

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        return options

    @property
    def odk_copies(self):
        odk_copies = PullODKData
        server_type = getattr(settings, 'ODK_SERVER_TYPE', '')
        if server_type:
            if server_type == 'aggregate':
                odk_copies = PullODKData
            if server_type == 'central':
                odk_copies = ODKCentralPullData
        return odk_copies

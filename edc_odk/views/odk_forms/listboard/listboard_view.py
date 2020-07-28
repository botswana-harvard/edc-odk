from django.contrib import messages
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import ListboardView as BaseListboardView
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_navbar import NavbarViewMixin

from edc_odk.model_wrappers import ConsentCopiesModelWrapper

from ....classes import PullODKData


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
    odk_copies = PullODKData

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        return options

    def get_context_data(self, **kwargs):
        c_count, c_updated = self.odk_copies(
            request=self.request).pull_consent_images_data()
        sc_count, sc_updated = self.odk_copies(
            request=self.request).pull_specimen_consent_images_data()
        cn_count, cn_updated = self.odk_copies(
            request=self.request).pull_clinician_notes_data()
        id_count, id_updated = self.odk_copies(
            request=self.request).pull_omang_images_data()

        count = c_count + sc_count + cn_count + id_count
        updated = c_updated + sc_updated + cn_updated + id_updated
        if count > 0:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                f'{count} record(s) downloaded successfully from the '
                f'odk aggregrate server.')
        if updated > 0:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                f'{updated} existing record(s) have been updated ')
        elif count == 0 and updated == 0:
            messages.add_message(
                self.request,
                messages.INFO,
                f'No new records found from the odk aggregrate.')
        context = super().get_context_data(**kwargs)

        return context

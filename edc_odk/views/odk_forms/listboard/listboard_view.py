from django.apps import apps as django_apps
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_dict = {}
        folders = self.check_is_folder()
        for folder in folders:
            obj_dict.update(
                {folder._meta.verbose_name: self.get_folder_objects(model_cls=folder)})
        context.update({'obj_dict': obj_dict})
        return context

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

    def all_odk_models(self):
        return list(django_apps.all_models['edc_odk'].values()) + self.app_models_cls()

    def check_is_folder(self):
        folderish = []
        for model in self.all_odk_models():
            for field in model._meta.fields:
                if field.name == 'subject_identifier':
                    folderish.append(model)
        return folderish

    def get_folder_objects(self, model_cls=None):
        return model_cls.objects.all()

    def app_config_models(self):
        config_list = []
        exclude = ('get_models', 'import_models')
        configs = django_apps.get_app_config('edc_odk')
        models_config = [config for config in dir(configs) if '_models' in config and config not in exclude]
        for config in models_config:
            config_dict = getattr(configs, config)
            for key, value in config_dict.items():
                config_list.append(f'{key}.{value}')
        return config_list

    def app_models_cls(self):
        model_cls = []
        for config in self.app_config_models():
            model = django_apps.get_model(config)
            model_cls.append(model)
        return model_cls

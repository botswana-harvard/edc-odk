from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(
        EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'edc_odk/odk_forms/home.html'
    navbar_name = 'edc_odk_forms'
    navbar_selected_item = 'edc_odk_usage'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

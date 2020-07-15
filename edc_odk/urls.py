from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import path
from django.views.generic.base import RedirectView
from edc_dashboard import UrlConfig
from .admin_site import edc_odk_admin
from .views import ListboardView, HomeView

app_name = 'edc_odk'

odk_listboard_url_config = UrlConfig(
    url_name='odk_listboard_url',
    view_class=ListboardView,
    label='edc_odk_listboard',
    identifier_label='subject_identifier',)

urlpatterns = [
    path('admin/', edc_odk_admin.urls),
    path('home/', HomeView.as_view(), name='home_url'),
    path('', RedirectView.as_view(url='admin/'), name='admin_url'), ]
urlpatterns += odk_listboard_url_config.listboard_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


odk_dashboard = Navbar(name='edc_odk_forms')

odk_dashboard.append_item(
    NavbarItem(
        name='edc_odk_forms',
        label='ODK Consents',
        fa_icon='fa fa-file-image',
        url_name=settings.DASHBOARD_URL_NAMES.get('odk_listboard_url')))

site_navbars.register(odk_dashboard)

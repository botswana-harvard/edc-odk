from edc_navbar import NavbarItem, site_navbars, Navbar


odk_dashboard = Navbar(name='edc_odk_forms')

odk_dashboard.append_item(
    NavbarItem(name='edc_odk_usage',
               label='EDC ODK Usage',
               fa_icon='fa-cogs',
               url_name='edc_odk:home_url'))

odk_dashboard.append_item(
    NavbarItem(name='edc_odk_admin',
               label='EDC ODK Admin',
               fa_icon='fa-cogs',
               url_name='edc_odk:admin_url'))

site_navbars.register(odk_dashboard)

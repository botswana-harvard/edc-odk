from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
    site_title = 'EDC ODK Forms'
    site_header = 'EDC ODK Forms'
    index_title = 'EDC ODK Forms'
    site_url = '/administration/'


edc_odk_admin = AdminSite(name='edc_odk_admin')

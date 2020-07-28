# edc-odk

EDC Open Data Kit Module

This module uses `django_q`.

A multiprocessing task queue for Django

## `Installation`

pip install django-q

pip install edc-odk

### `Usage`

Add `django_q` and `edc_odk.apps.AppConfig` to INSTALLED_APPS in your Django project settings, django-q configuration is handled via the Q_CLUSTER dictionary; all configurations are optional see [https://django-q.readthedocs.io/en/latest/configure.html](https://django-q.readthedocs.io/en/latest/configure.html) for configuration options.

	`settings.py`
	
		....	
		APP_NAME = 'your_app_name'
		
		INSTALLED_APPS = (
		  ...
		  'django_q',
		  'edc_odk.apps.AppConfig',
		)

		ODK_CONFIGURATION = {
    			'OPTIONS': {
            		'read_default_file': '/etc/odk/odk.cnf',
    			},
		}
		
		BASE_FORMAT = 'https://%(host)s/view/%(api)s?formId=%(form_id)s'
		
		# django_q configuration
		Q_CLUSTER = {
		    'name': 'your_app_name',
		    'workers': 4,
		    'orm': 'default'
		    ....
		}
		
		DASHBOARD_URL_NAMES = {
			...
		    'odk_listboard_url': 'edc_odk:odk_listboard_url',
		}
		
		
		DASHBOARD_BASE_TEMPLATES = {
			....
		    'odk_listboard_template': 'edc_odk/odk_forms/listboard.html',
		}
	
	`project.cnf` This is placed outside the project since it holds sensitive information
	
		[read]
		host = '' # This hold the ip or domain name your odk aggregate instance
		user = '' # The admin username for your instance
		pw = **** # The admin user password

Run migrations:


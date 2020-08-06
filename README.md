# edc-odk

EDC Open Data Kit Module

This module uses `django_q`.

A multiprocessing task queue for Django

## `Installation`

pip install Celery

pip install edc-odk

## `Install RabbitMQ for the celery broker`

apt-get install rabbitmq-server

brew install rabbitmq | on macos

Start the rabbitMQ server

### `Usage`

Add `edc_odk.apps.AppConfig` to INSTALLED_APPS and celery configurations in your Django project settings.

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
		
		# celery configuration
		CELERY_BROKER_URL = 'amqp://localhost'
		CELERY_INCLUDE = ['myapp.tasks', ]
		
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

	`celery.py` Setup your celery instance in your proj app dir
		import os
		from celery import Celery
		os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproj.settings')
		
		app = Celery('myproj')
		app.config_from_object('django.conf:settings', namespace='CELERY')
		app.autodiscover_tasks()

Run migrations:


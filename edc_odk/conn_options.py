import configparser
from django.conf import settings


class ODKConnectionOptions:
    config = configparser.ConfigParser()

    settings_dict = settings.ODK_CONFIGURATION
    config_file = settings_dict['OPTIONS'].get('read_default_file')
    config.read(config_file)
    if config_file:
        host = config['read']['host']
        user = config['read']['user']
        password = config['read']['pw']

from __future__ import absolute_import
from os import environ
import dj_database_url

from django.core.exceptions import ImproperlyConfigured

from .base import *

DEBUG = False

DATABASE_URL = environ.get('DATABASE_URL')
DATABASES['default'] = dj_database_url.config(default=DATABASE_URL,
                                              conn_max_age=500)


def get_env_setting(setting):
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_env_setting('SECRET_KEY')

ROLLBAR = {
    'access_token': '174e388b95d54725822b0997121c70ce',
    'environment': 'production',
    'branch': 'master',
    'root': os.getcwd(),
}

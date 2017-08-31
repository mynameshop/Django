from .base import *

DEBUG = True
DEBUG404 = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += ("debug_toolbar", )
SITE_ID = 4
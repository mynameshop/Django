from .base import *

DEBUG = True


INSTALLED_APPS += ("debug_toolbar", "performance_test", )
SITE_ID = 4

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'maciek YS testing <m@il.xx>'

NOTIFICATIONS_EMAIL_TARGET = 'irvrsfod@sharklasers.com'
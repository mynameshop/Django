# SECURITY WARNING: keep the secret key used in production secret!
from .utils import BASE_DIR
import os
SECRET_KEY = '(k%61$%)o+8)bl5x#p45=6!179bax#qewkd1=tj&ay7j8c#)a+'

DEBUG = True
ALLOWED_HOSTS = ['*',]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/projects/'
LOGOUT_URL = '/logout/'
LOGOUT_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = ('apps.accounts.backends.UserBackend',)

DEPLOY_SCRIPT_PATH = os.path.join(BASE_DIR, '../deploy.sh')
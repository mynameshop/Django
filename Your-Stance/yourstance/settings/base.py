import os
from os.path import abspath, dirname, join, normpath
DEBUG404 = False
DJANGO_ROOT = dirname(dirname(abspath(__file__)))
SITE_ROOT = dirname(DJANGO_ROOT)
SITE_NAME = 'yourstance'
# path.append(DJANGO_ROOT)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../..'))
ABS_TEMPLATES_PATH = '%s/templates' % ABS_PROJECT_ROOT

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = 'bb@416)g%mgj6r8^28e%b@3ktm3^3qpp(+$m_($1_ih8jwz%(b'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Tyler Waitt', 'tylerwaitt@gmail.com'),
)
MANAGERS = ADMINS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'storages',
    'imagekit',
    'django_ses',
    'loginas',
    'django_nose',
    'reversion',

    'home',
    'pages',
    'forums',
    'questions',
    'questionlists',
    'profiles',
    'organizations',
    'stances',
    'user_settings',
    'onboarding',
    'common',
    'notifications',
    'badges.apps.BadgesConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'yourstance.middleware.proxycheck.ProxyUserCheckMiddleware',
    'yourstance.middleware.wedge.FbWedgeCheckMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]

ROOT_URLCONF = 'yourstance.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ABS_TEMPLATES_PATH],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
    'django.template.loaders.app_directories.load_template_source',
)

WSGI_APPLICATION = 'yourstance.wsgi.application'

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'yourstance',
#        'USER': 'postgres',
#        'PASSWORD': 'postgres',
#        'HOST': '127.0.0.1',
#        'PORT': '5432',
#    }
#}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'yourinstance',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = normpath(join(SITE_ROOT, 'staticfiles'))
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    normpath(join(SITE_ROOT, 'static')),
]

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# AllAuth settings
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_ADAPTER = "profiles.adapter.Adapter"
SITE_ID = 3
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_birthday', 'user_friends', 'user_photos'],
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
            'friends',
        ],
        'EXCHANGE_TOKEN': True,
        'VERSION': 'v2.4'
    },
    'google': {
        'SCOPE': ['profile', 'email', 'https://www.googleapis.com/auth/contacts'],
        'AUTH_PARAMS': {'access_type': 'online'}
    },
    'twitter': {
        'SCOPE': ['profile', 'email']
    }
}

# storages
# DEFAULT_FILE_STORAGE = 'libs.storages.S3Storage.S3Storage'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# AWS
AWS_ACCESS_KEY_ID = 'AKIAJIDUDHFFVHXJYU2A'
AWS_SECRET_ACCESS_KEY = 'HCB2EIS5JgpTHx/fHhL7+dMVzvzZf+y0ZXOhWC3n'
AWS_STORAGE_BUCKET_NAME = 'yourstance-dev'

# Choices
PRO = 'p'
CON = 'c'
UNSURE = 'u'
QUESTION_CHOICES = (
    (PRO, 'Pro'),
    (CON, 'Con'),
    (UNSURE, 'Unsure'),
)

MAX_COMMENT_DEPTH = 3

EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = environ.get('EMAIL_HOST', 'email-smtp.us-east-1.amazonaws.com')
# EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', 'Ak3XLSjqs9SJfEgmBBbtEdWHUbP91NTH05EpPiLM3o3F')
# EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'AKIAJ4APKIHCGCJEBVJQ')
# EMAIL_PORT = environ.get('EMAIL_PORT', 587)
EMAIL_SUBJECT_PREFIX = 'yourstance'
EMAIL_USE_TLS = True
# SERVER_EMAIL = EMAIL_HOST_USER

SESSION_COOKIE_AGE = 31536000
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
LOGIN_URL = 'pages:login'

# ROLLBAR = {
#     'access_token': '174e388b95d54725822b0997121c70ce',
#     'environment': 'development',
#     'branch': 'master',
#     'root': os.getcwd(),
# }

NOTIFICATIONS_EMAIL_TARGET = None

import os
from .utils import BASE_DIR
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'apps', 'canvas_gadget', 'templates'),
            os.path.join(BASE_DIR, 'apps', 'feedback', 'templates')
        ],
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
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'apps.base.jinja2_environment.environment',
            'extensions': [
                'compressor.contrib.jinja2ext.CompressorExtension',
                'jinja2.ext.i18n',
                'jinja2.ext.with_',
            ],
        }
    },
]
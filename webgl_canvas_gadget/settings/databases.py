# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'canvas_gadget',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.01',
        'PORT': '5432',
        'CONN_MAX_AGE': 500,
    },
}
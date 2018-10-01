from .base import *

SECRET_KEY = config('SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['contactcongress.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'contactcongress',
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),

    }
}


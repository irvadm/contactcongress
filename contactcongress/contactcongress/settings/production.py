from .base import *

SECRET_KEY = config('SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['contactcongress.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500

from .base import *
from decouple import config as decouple_config
import dj_database_url

DEBUG = decouple_config('DEBUG')

SECRET_KEY = decouple_config('SECRET_KEY')

ALLOWED_HOSTS = ['contactcongress.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES['default'] = dj_database_url.config(decouple_config('DATABASE_URL'))
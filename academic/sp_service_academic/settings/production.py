from .base import *
import os
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=['http://*','https://*']
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['ACADEMIC_DBNAME'],
        'HOST': os.environ['ACADEMIC_DBHOST'],
        'USER': os.environ['ACADEMIC_DBUSER'],
        'PASSWORD': os.environ['ACADEMIC_DBPASS']
    }
}

CACHES = {
    'default': {
        'BACKEND': 'djpymemcache.backend.PyMemcacheCache',
        'LOCATION': [
        '127.0.0.1:11211',
        ],
    },
}

import os
from datetime import timedelta
from .base import *

#development key
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['USER_DBNAME'],
        'HOST': os.environ['USER_DBHOST'],
        'USER': os.environ['USER_DBUSER'],
        'PASSWORD': os.environ['USER_DBPASS'] 
    }
}

SIMPLE_JWT = {
    'SIGNING_KEY': os.environ['SECRET_KEY'],
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=30),
}

import os, json
from datetime import timedelta
from .base import *

#production key
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

CORS_ALLOWED_ORIGINS= json.loads(os.environ["CORS_ALLOWED_ORIGINS"])
ALLOWED_HOSTS = json.loads(os.environ["ALLOWED_HOSTS"])

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
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=10),
}

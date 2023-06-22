import os
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
        'NAME': os.environ['PROJECT_DBNAME'],
        'HOST': os.environ['PROJECT_DBHOST'],
        'USER': os.environ['PROJECT_DBUSER'],
        'PASSWORD': os.environ['PROJECT_DBPASS'] 
    }
}

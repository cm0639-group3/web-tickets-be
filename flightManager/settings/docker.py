import os
from .defaults import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': os.environ.get('DB_NAME'),
        'USER':os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST':os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}

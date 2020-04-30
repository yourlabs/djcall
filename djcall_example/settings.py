# flake8: noqa: D*
import os
from crudlfap.settings import *

DEBUG = True

ROOT_URLCONF = 'djcall_example.urls'

INSTALLED_APPS += ['djcall']

STATIC_ROOT = 'static'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': os.getenv('POSTGRES_USER', os.getenv('USER')),
        'NAME': os.getenv('POSTGRES_DB', 'djcall'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', None),
        'HOST': os.getenv('POSTGRES_HOST', None),
    }
}

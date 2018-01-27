import os
import json
from pprint import pprint as pp

from .settings import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False

ALLOWED_HOSTS = ['*']

data = json.load(open(BASE_DIR +'/settings/production.json'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': data['postgres']['db'],
        'USER': data['postgres']['user'],
        'PASSWORD': data['postgres']['pass'],
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

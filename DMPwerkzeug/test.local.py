# coding=utf8
import os,sys

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

SECRET_KEY = 'this is a not very secret key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DMPwerkzeug',
        'USER': 'postgres'
    }
}

SITE_TITLE = 'DMPwerkzeug'
SITE_ROOT = os.path.dirname(os.path.dirname(__file__))
SITE_URL = 'http://localhost:8000'

TIME_ZONE = 'Europe/Berlin'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FROM = 'info@example.com'

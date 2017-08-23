from .base import INSTALLED_APPS

DEBUG = True

SECRET_KEY = 'this is a not very secret key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rdmo',
        'USER': 'postgres'
    }
}

INSTALLED_APPS += [
    'allauth',
    'allauth.account'
]

ACCOUNT = True
ACCOUNT_SIGNUP = True
SOCIALACCOUNT = False

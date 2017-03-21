from .base import INSTALLED_APPS

DEBUG = True

SECRET_KEY = 'this is a not very secret key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

INSTALLED_APPS += [
    'allauth',
    'allauth.account'
]

ACCOUNT = True
ACCOUNT_SIGNUP = True
SOCIALACCOUNT = False

from .base import INSTALLED_APPS

DEBUG = True

SECRET_KEY = 'this is a not very secret key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rdmo',
        'USER': 'root',
        'PASSWORD': ''
    }
}

INSTALLED_APPS += [
    'allauth',
    'allauth.account'
]

ACCOUNT = True
ACCOUNT_SIGNUP = True
SOCIALACCOUNT = False

# coding=utf-8
import os

DEBUG = True
#DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', 'dmp']

SECRET_KEY = 'this is a not very secret key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dmpwerkzeug',
        'USER': 'dmpwerkzeug',
        'PASSWORD': 'dmpwerkzeug',
        'HOST': '127.0.0.1'
    }

    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'dmpwerkzeug',
    #     'USER': 'dmpwerkzeug',
    #     'PASSWORD': 'dmpwerkzeug'
    # }

    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(SITE_ROOT, 'db.sqlite3')
    # }
}

EMAIL_FROM = 'info@example.com'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

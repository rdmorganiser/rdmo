# coding=utf-8
import os
from django.utils.translation import ugettext_lazy as _

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

SECRET_KEY = 'this is a not very secret key'

SITE_TITLE = 'DMPwerkzeug'
SITE_ROOT = os.path.dirname(os.path.dirname(__file__))
SITE_URL = 'http://localhost:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DMPwerkzeug',
        'USER': 'postgres'
    }
}

TIME_ZONE = 'Europe/Berlin'

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('de', _('German')),
    ('en', _('English')),
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FROM = 'info@example.com'

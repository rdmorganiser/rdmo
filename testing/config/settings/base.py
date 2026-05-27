import os
from warnings import filterwarnings

from django.utils.translation import gettext_lazy as _

DEBUG = os.getenv("DJANGO_DEBUG", False) == "True"
TEMPLATE_DEBUG = False
DEBUG_LOGGING = False

SECRET_KEY = "this is a not very secret key"

GITHUB_DB_BACKEND = os.getenv('GITHUB_DB_BACKEND')
if GITHUB_DB_BACKEND == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'rdmo',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': '127.0.0.1',
            'TEST': {
                'CHARSET': 'utf8',
                'COLLATION': 'utf8_general_ci',
            },
            'OPTIONS': {
                'init_command': "SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));"
            }
        }
    }
elif GITHUB_DB_BACKEND == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'rdmo',
            'USER': 'postgres_user',
            'PASSWORD': 'postgres_password',
            'HOST': '127.0.0.1',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

FIXTURE_DIRS = (
    BASE_DIR / 'fixtures',
)

INSTALLED_APPS += [
    'allauth',
    'allauth.account',
    "allauth.socialaccount",
    "allauth.socialaccount.providers.dummy",
]

MIDDLEWARE += [
    'allauth.account.middleware.AccountMiddleware'
]

ACCOUNT = True
ACCOUNT_SIGNUP = True
SOCIALACCOUNT = False

INSTALLED_APPS += [
    'drf_spectacular',
    'drf_spectacular_sidecar'
]

REST_FRAMEWORK.update({
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ('v1', ),
})

PROJECT_TABLE_PAGE_SIZE = 5

PROJECT_SEND_ISSUE = True

PROJECT_SEND_INVITE = True

EMAIL_RECIPIENTS_CHOICES = [
    ('email@example.com', 'Emmi Email <email@example.com>'),
]
EMAIL_RECIPIENTS_INPUT = True

INSTALLED_APPS += [
    'plugins',  # introduced in 2.5, rdmo/testing/plugins
]

PLUGINS = [  # introduced in 2.5
    # internal rdmo plugins
    'rdmo.projects.exports.RDMOXMLExport',
    'rdmo.projects.exports.CSVCommaExport',
    'rdmo.projects.exports.CSVSemicolonExport',
    'rdmo.projects.exports.JSONExport',
    'rdmo.projects.imports.RDMOXMLImport',
    'rdmo.projects.imports.URLImport',
    # rdmo/testing/plugins
    'plugins.optionset_providers.providers.SimpleProvider',  # here or in app/test
    'plugins.project_issue_providers.providers.SimpleIssueProvider',
    'plugins.project_export.exports.SimpleExportPlugin',
    'plugins.project_snapshot_export.exports.SimpleSnapshotExportPlugin',
    'plugins.project_import.imports.SimpleImportPlugin',
]

PROJECT_VALUES_VALIDATION = True

PROJECT_CONTACT = True
PROJECT_CONTACT_RECIPIENTS = ['email@example.com']

# Ref: https://adamj.eu/tech/2023/12/07/django-fix-urlfield-assume-scheme-warnings
filterwarnings(
    "ignore", "The FORMS_URLFIELD_ASSUME_HTTPS transitional setting is deprecated."
)
# This value will change from False to True in Django 6.0
# Refs:
# - https://docs.djangoproject.com/en/5.2/ref/settings/#forms-urlfield-assume-https
# - https://docs.djangoproject.com/en/5.2/ref/forms/fields/#django.forms.URLField.assume_scheme
FORMS_URLFIELD_ASSUME_HTTPS = True

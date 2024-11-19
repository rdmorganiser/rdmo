import os

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
    'allauth.account'
]

MIDDLEWARE += [
    'allauth.account.middleware.AccountMiddleware'
]

ACCOUNT = True
ACCOUNT_SIGNUP = True
SOCIALACCOUNT = False

PROJECT_TABLE_PAGE_SIZE = 5

PROJECT_SEND_ISSUE = True

PROJECT_SEND_INVITE = True

PROJECT_REMOVE_VIEWS = True

PROJECT_SNAPSHOT_EXPORTS = [
    ('xml', _('RDMO XML'), 'rdmo.projects.exports.RDMOXMLExport'),
]

EMAIL_RECIPIENTS_CHOICES = [
    ('email@example.com', 'Emmi Email <email@example.com>'),
]
EMAIL_RECIPIENTS_INPUT = True

OPTIONSET_PROVIDERS = [
    ('simple', _('Simple provider'), 'rdmo.options.providers.SimpleProvider')
]

PROJECT_ISSUE_PROVIDERS = [
    ('simple', _('Simple provider'), 'rdmo.projects.providers.SimpleIssueProvider')
]

PROJECT_IMPORTS += [
    ('url', _('from URL'), 'rdmo.projects.imports.URLImport'),
]

PROJECT_IMPORTS_LIST = ['url']

PROJECT_VALUES_VALIDATION = True

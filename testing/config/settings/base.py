import os

from django.utils.translation import gettext_lazy as _

DEBUG = False
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

PROJECT_SEND_ISSUE = True

PROJECT_SEND_INVITE = True

PROJECT_REMOVE_VIEWS = True

EMAIL_RECIPIENTS_CHOICES = [
    ('email@example.com', 'Emmi Email <email@example.com>'),
]
EMAIL_RECIPIENTS_INPUT = True

PROJECT_ISSUE_PROVIDERS = [
    ('github', _('GitHub'), 'rdmo.projects.providers.GitHubIssueProvider')
]

GITHUB_PROVIDER = {
    'client_id': '',
    'client_secret': ''
}

'''
LOGGING
'''
LOGGING_DIR = BASE_DIR / 'log'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s'
        },
        'name': {
            'format': '[%(asctime)s] %(levelname)s %(name)s: %(message)s'
        },
        'console': {
            'format': '[%(asctime)s] %(message)s'
        },
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(filename)s %(lineno)d: %(message)s',
            'datefmt': '%H:%M:%S'
        },
        'fullverbose': {
            'format': '%(asctime)s [%(levelname)s] %(pathname)s %(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'error_log': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOGGING_DIR / 'rdmo_error.log',
            'formatter': 'default'
        },
        'rdmo_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGGING_DIR / 'rdmo.log',
            'formatter': 'fullverbose'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins', 'error_log'],
            'level': 'ERROR',
            'propagate': True
        },
        'rdmo': {
            'handlers': ['rdmo_log'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

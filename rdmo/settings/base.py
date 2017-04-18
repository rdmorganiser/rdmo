import os
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _

SITE_ID = 1

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SECRET_KEY = 'this is not a very secret key'

DEBUG = False

ALLOWED_HOSTS = ['localhost']

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS = [
    # django modules
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # rdmo modules
    'apps.core',
    'apps.accounts',
    'apps.domain',
    'apps.options',
    'apps.conditions',
    'apps.questions',
    'apps.tasks',
    'apps.views',
    'apps.projects',
    # 3rd party modules
    'rest_framework',
    'rest_framework.authtoken',
    'widget_tweaks',
    'markdown',
    'compressor',
    'djangobower',
    'mptt',
    'rules'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware'
]

ROOT_URLCONF = 'rdmo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
            ],
        },
    },
]

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

WSGI_APPLICATION = 'rdmo.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTHENTICATION_BACKENDS = [
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend'
]

PROFILE_UPDATE = True

ACCOUNT = False
ACCOUNT_SIGNUP = False
SOCIALACCOUNT = False
SHIBBOLETH = False

ACCOUNT_SIGNUP_FORM_CLASS = 'apps.accounts.forms.SignupForm'
ACCOUNT_USER_DISPLAY = 'apps.accounts.utils.get_full_name'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_ACTIVATION_DAYS = 7
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_PASSWORD_MIN_LENGTH = 4

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

LANGUAGES = (
    ('de', _('German')),
    ('en', _('English')),
)

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/account/logout/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root/')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    'djangobower.finders.BowerFinder',
)

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components_root/')

BOWER_INSTALLED_APPS = (
    "angular#~1.5.8",
    "bootstrap#~3.3.7",
    "angular-resource#~1.5.8",
    "codemirror#~5.18.2",
    "components-font-awesome#~4.6.3",
    "bootstrap-datepicker#~1.6.4",
    "moment#~2.14.1"
)

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'testing/fixtures/'),
)

CACHE_TIMEOUT = 60

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'rdmo_default'
    },
    'api': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'rdmo_api'
    }
}

REST_FRAMEWORK = {
    'UNICODE_JSON': False,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning'
}

REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': CACHE_TIMEOUT
}

SETTINGS_EXPORT = [
    'LOGIN_URL',
    'LOGOUT_URL',
    'ACCOUNT',
    'ACCOUNT_SIGNUP',
    'SOCIALACCOUNT',
    'PROFILE_UPDATE',
    'SHIBBOLETH'
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FROM = 'info@example.com'

EXPORT_FORMATS = OrderedDict((
    ('pdf', _('PDF')),
    ('rtf', _('Rich Text Format')),
    ('odt', _('Open Office')),
    ('docx', _('Microsoft Office')),
    ('html', _('HTML')),
    ('markdown', _('Markdown')),
    ('mediawiki', _('mediawiki')),
    ('tex', _('LaTeX'))
))

DEFAULT_URI_PREFIX = 'http://example.com/terms'

# try override with the local configuration
try:
    from .local import *
except ImportError:
    pass

# add static and templates from local.THEME_DIR to STATICFILES_DIRS and TEMPLATES
try:
    STATICFILES_DIRS = [
        os.path.join(THEME_DIR, 'static/')
    ]
    TEMPLATES[0]['DIRS'].append(os.path.join(THEME_DIR, 'templates/'))
except NameError:
    pass

# prepend the local.BASE_URL to the different URL settings
try:
    LOGIN_URL = BASE_URL + LOGIN_URL
    LOGIN_REDIRECT_URL = BASE_URL + LOGIN_REDIRECT_URL
    LOGOUT_URL = BASE_URL + LOGOUT_URL
    ACCOUNT_LOGOUT_REDIRECT_URL = BASE_URL
    MEDIA_URL = BASE_URL + MEDIA_URL
    STATIC_URL = BASE_URL + STATIC_URL

    CSRF_COOKIE_PATH = BASE_URL + '/'
    LANGUAGE_COOKIE_PATH = BASE_URL + '/'
    SESSION_COOKIE_PATH = BASE_URL + '/'
except NameError:
    pass

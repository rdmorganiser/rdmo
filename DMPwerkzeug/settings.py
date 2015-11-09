import os
from local import *

INSTALLED_APPS = (
    # django modules
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party modules
    'rest_framework',
    'widget_tweaks',
    'markdown',
    'compressor',
    'registration',
    # DMPwerkzeug modules
    'core'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'DMPwerkzeug.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SITE_ROOT, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.settings'
            ],
        },
    },
]

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

WSGI_APPLICATION = 'DMPwerkzeug.wsgi.application'

INTERNAL_IPS = ('127.0.0.1',)

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media_root/')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'static_root/')

STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

LOGOUT_URL = '/logout'

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_EMAIL_HTML = False

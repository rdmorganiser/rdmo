from django.utils.translation import ugettext_lazy as _

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
    'rdmo.core',
    'rdmo.accounts',
    'rdmo.domain',
    'rdmo.options',
    'rdmo.conditions',
    'rdmo.questions',
    'rdmo.tasks',
    'rdmo.views',
    'rdmo.projects',
    # 3rd party modules
    'rest_framework',
    'rest_framework.authtoken',
    'widget_tweaks',
    'markdown',
    'compressor',
    'django_extensions',
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend'
]

PROFILE_UPDATE = True

ACCOUNT = False
ACCOUNT_SIGNUP = False
SOCIALACCOUNT = False
SHIBBOLETH = False

ACCOUNT_SIGNUP_FORM_CLASS = 'rdmo.accounts.forms.SignupForm'
ACCOUNT_USER_DISPLAY = 'rdmo.accounts.utils.get_full_name'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_ACTIVATION_DAYS = 7
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_PASSWORD_MIN_LENGTH = 4

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

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
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3'
    }
}

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
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60
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

EXPORT_FORMATS = (
    ('pdf', _('PDF')),
    ('rtf', _('Rich Text Format')),
    ('odt', _('Open Office')),
    ('docx', _('Microsoft Office')),
    ('html', _('HTML')),
    ('markdown', _('Markdown')),
    ('mediawiki', _('mediawiki')),
    ('tex', _('LaTeX'))
)

DEFAULT_URI_PREFIX = 'http://example.com/terms'

VENDOR_CDN = True

VENDOR = {
    'jquery': {
        'url': 'https://code.jquery.com/',
        'js': [
            {
                'path': 'jquery-3.2.1.min.js',
                'sri': 'sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=',
            }
        ]
    },
    'bootstrap': {
        'url': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/',
        'js': [
            {
                'path': 'js/bootstrap.min.js',
                'sri': 'sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa',
            }
        ],
        'css': [
            {
                'path': 'css/bootstrap.min.css',
                'sri': 'sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u',
            }
        ]
    },
    'bootstrap-datepicker': {
        'url': 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.7.1/',
        'css': [
            {
                'path': 'css/bootstrap-datepicker.min.css'
            }
        ],
        'js': [
            {
                'path': 'js/bootstrap-datepicker.min.js'
            }
        ]
    },
    'font-awesome': {
        'url': 'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/',
        'css': [
            {
                'path': 'css/font-awesome.min.css'
            }
        ],
        'font': [
            {
                'path': 'fonts/fontawesome-webfont.eot'
            },
            {
                'path': 'fonts/fontawesome-webfont.woff2'
            },
            {
                'path': 'fonts/fontawesome-webfont.woff'
            },
            {
                'path': 'fonts/fontawesome-webfont.ttf'
            },
            {
                'path': 'fonts/fontawesome-webfont.svg'
            }
        ]
    },
    'angular': {
        'url': 'https://ajax.googleapis.com/ajax/libs/angularjs/1.5.8/',
        'js': [
            {
                'path': 'angular.min.js'
            },
            {
                'path': 'angular-resource.min.js'
            }
        ]
    },
    'moment': {
        'url': 'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/',
        'js': [
            {
                'path': 'moment.min.js',
                'sri': 'sha256-1hjUhpc44NwiNg8OwMu2QzJXhD8kcj+sJA3aCQZoUjg='
            }
        ]
    },
    'codemirror': {
        'url': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/',
        'js': [
            {
                'path': 'codemirror.min.js',
                'sri': 'sha256-0LRLvWWVXwt0eH0/Bzd0PHICg/bSMDIe5sXgaDSpZaA='
            },
            {
                'path': 'addon/mode/overlay.min.js',
                'sri': 'sha256-ffWkw3Pn4ieMygm1vwdRKcMtBJ6E6kuBi8GlVVPXWEs='
            },
                        {
                'path': 'mode/django/django.min.js',
                'sri': 'sha256-6hO1TjC+3W73p+kXnCqcHVjfRa4KMdG7hvWencnu0XM='
            }
        ],
        'css': [
            {
                'path': 'codemirror.min.css',
                'sri': 'sha256-wluO/w4cnorJpS0JmcdTSYzwdb5E6u045qa4Ervfb1k='
            }
        ]
    }
}

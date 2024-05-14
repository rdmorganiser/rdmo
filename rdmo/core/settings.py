from django.utils.translation import gettext_lazy as _

SITE_ID = 1

DEBUG = False

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
    'rdmo',
    'rdmo.core',
    'rdmo.overlays',
    'rdmo.accounts',
    'rdmo.services',
    'rdmo.domain',
    'rdmo.options',
    'rdmo.conditions',
    'rdmo.questions',
    'rdmo.tasks',
    'rdmo.views',
    'rdmo.projects',
    'rdmo.management',
    # 3rd party modules
    'rest_framework',
    'rest_framework.authtoken',
    'widget_tweaks',
    'markdown',
    'compressor',
    'django_cleanup',
    'django_extensions',
    'django_filters',
    'mathfilters',
    'mptt',
    'rules',
    # openapi specification tools
    'rest_framework_swagger'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
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

MULTISITE = False

GROUPS = False

LOGIN_FORM = True

PROFILE_UPDATE = True
PROFILE_DELETE = True

ACCOUNT = False
ACCOUNT_SIGNUP = False
ACCOUNT_GROUPS = []
ACCOUNT_TERMS_OF_USE = False
ACCOUNT_ADAPTER = 'rdmo.accounts.adapter.AccountAdapter'
ACCOUNT_SIGNUP_FORM_CLASS = 'rdmo.accounts.forms.SignupForm'
ACCOUNT_USER_DISPLAY = 'rdmo.accounts.utils.get_full_name'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_ACTIVATION_DAYS = 7
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_PASSWORD_MIN_LENGTH = 4
ACCOUNT_EMAIL_MAX_LENGTH = 190
ACCOUNT_PREVENT_ENUMERATION = False
ACCOUNT_ALLOW_USER_TOKEN = False

SOCIALACCOUNT = False
SOCIALACCOUNT_SIGNUP = False
SOCIALACCOUNT_GROUPS = []
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_ADAPTER = 'rdmo.accounts.adapter.SocialAccountAdapter'

SHIBBOLETH = False
SHIBBOLETH_LOGIN_URL = '/Shibboleth.sso/Login'
SHIBBOLETH_LOGOUT_URL = '/Shibboleth.sso/Logout'
SHIBBOLETH_USERNAME_PATTERN = None

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

LANGUAGES = (
    ('en', _('English')),
    ('de', _('German')),
)

USE_I18N = True

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
    }
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'UNICODE_JSON': False,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

SETTINGS_EXPORT = [
    'SITE_ID',
    'LOGIN_URL',
    'LOGOUT_URL',
    'LOGIN_FORM',
    'ACCOUNT',
    'ACCOUNT_SIGNUP',
    'ACCOUNT_TERMS_OF_USE',
    'ACCOUNT_ALLOW_USER_TOKEN',
    'SOCIALACCOUNT',
    'PROFILE_UPDATE',
    'PROFILE_DELETE',
    'SHIBBOLETH',
    'SHIBBOLETH_LOGIN_URL',
    'MULTISITE',
    'GROUPS',
    'EXPORT_FORMATS',
    'PROJECT_ISSUES',
    'PROJECT_VIEWS',
    'PROJECT_EXPORTS',
    'PROJECT_IMPORTS',
    'PROJECT_IMPORTS_LIST',
    'PROJECT_SEND_ISSUE',
    'PROJECT_QUESTIONS_AUTOSAVE',
    'NESTED_PROJECTS'
]

SETTINGS_API = [
    'PROJECT_QUESTIONS_AUTOSAVE',
    'PROJECT_QUESTIONS_CYCLE_SETS',
    'DEFAULT_URI_PREFIX',
    'LANGUAGES',
    'MULTISITE',
    'GROUPS',
    'EXPORT_FORMATS',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'info@example.com'

EMAIL_RECIPIENTS_CHOICES = []
EMAIL_RECIPIENTS_INPUT = False

USER_API = True

OVERLAYS = {
    'projects': [
        'projects-table',
        'create-project',
        'import-project',
        'support-info'
    ],
    'project': [
        'project-questions',
        'project-catalog',
        'project-issues',
        'project-views',
        'project-memberships',
        'project-snapshots',
        'export-project',
        'import-project',
        'support-info'
    ],
    'issue_send': [
        'issue-message',
        'issue-attachments',
        'support-info'
    ]
}

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

EXPORT_REFERENCE_ODT_VIEWS = {}
EXPORT_REFERENCE_DOCX_VIEWS = {}
EXPORT_REFERENCE_ODT = None
EXPORT_REFERENCE_DOCX = None

EXPORT_PANDOC_ARGS = {
    'pdf': ['-V', 'geometry:a4paper, margin=1in', '--pdf-engine=xelatex'],
    'rtf': ['--standalone']
}

EXPORT_CONTENT_DISPOSITION = 'attachment'

PROJECT_ISSUES = True

PROJECT_ISSUE_PROVIDERS = []

PROJECT_VIEWS = True

PROJECT_EXPORTS = [
    ('xml', _('RDMO XML'), 'rdmo.projects.exports.RDMOXMLExport'),
    ('csvcomma', _('CSV (comma separated)'), 'rdmo.projects.exports.CSVCommaExport'),
    ('csvsemicolon', _('CSV (semicolon separated)'), 'rdmo.projects.exports.CSVSemicolonExport'),
    ('json', _('JSON'), 'rdmo.projects.exports.JSONExport'),
]

PROJECT_IMPORTS = [
    ('xml', _('RDMO XML'), 'rdmo.projects.imports.RDMOXMLImport'),
]

PROJECT_IMPORTS_LIST = []

PROJECT_QUESTIONS_AUTOSAVE = True

PROJECT_QUESTIONS_CYCLE_SETS = False

PROJECT_FILE_QUOTA = '10Mb'

PROJECT_SEND_ISSUE = False

PROJECT_INVITE_TIMEOUT = None

PROJECT_SEND_INVITE = True

PROJECT_REMOVE_VIEWS = True

PROJECT_CREATE_RESTRICTED = False
PROJECT_CREATE_GROUPS = []

PROJECT_VALUES_CONFLICT_THRESHOLD = 0.01

NESTED_PROJECTS = True

OPTIONSET_PROVIDERS = []

QUESTIONS_WIDGETS = [
    ('text', _('Text'), 'rdmo.projects.widgets.TextWidget'),
    ('textarea', _('Textarea'), 'rdmo.projects.widgets.TextareaWidget'),
    ('yesno', _('Yes/No'), 'rdmo.projects.widgets.YesnoWidget'),
    ('checkbox', _('Checkboxes'), 'rdmo.projects.widgets.CheckboxWidget'),
    ('radio', _('Radio buttons'), 'rdmo.projects.widgets.RadioWidget'),
    ('select', _('Select drop-down'), 'rdmo.projects.widgets.SelectWidget'),
    ('autocomplete', _('Autocomplete'), 'rdmo.projects.widgets.AutocompleteWidget'),
    ('freeautocomplete', _('Free autocomplete'), 'rdmo.projects.widgets.FreeAutocompleteWidget'),
    ('range', _('Range slider'), 'rdmo.projects.widgets.RangeWidget'),
    ('date', _('Date picker'), 'rdmo.projects.widgets.DateWidget'),
    ('file', _('File upload'), 'rdmo.projects.widgets.FileWidget')
]

DEFAULT_URI_PREFIX = 'http://example.com/terms'

REPLACE_MISSING_TRANSLATION = False

VENDOR_CDN = True

VENDOR = {
    'jquery': {
        'url': 'https://code.jquery.com/',
        'js': [
            {
                'path': 'jquery-3.4.1.min.js',
                'sri': 'sha384-vk5WoKIaW/vJyUAd9n/wmopsmNhiy+L2Z+SBxGYnUkunIxVxAv/UtMOhba/xskxh',
            }
        ]
    },
    'bootstrap': {
        'url': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/',
        'js': [
            {
                'path': 'js/bootstrap.min.js',
                'sri': 'sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd',
            }
        ],
        'css': [
            {
                'path': 'css/bootstrap.min.css',
                'sri': 'sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu',
            }
        ],
        'font': [
            {
                'path': 'fonts/glyphicons-halflings-regular.eot'
            },
            {
                'path': 'fonts/glyphicons-halflings-regular.woff'
            },
            {
                'path': 'fonts/glyphicons-halflings-regular.woff2'
            },
            {
                'path': 'fonts/glyphicons-halflings-regular.ttf'
            },
            {
                'path': 'fonts/glyphicons-halflings-regular.svg'
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
    'select2': {
        'url': 'https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/',
        'js': [
            {
                'path': 'js/select2.min.js',
                'sri': 'sha256-HNkbndPiWM5EIRgahc3hWiuGD6CtwFgMfEU0o3zeabo='
            }
        ],
        'css': [
            {
                'path': 'css/select2.min.css',
                'sri': 'sha256-EQA4j7+ZbrewCQvwJzNmVxiKMwGRspXMGgt7I6AAiqs='
            }
        ]
    },
    'select2-bootstrap-theme': {
        'url': 'https://cdnjs.cloudflare.com/ajax/libs/select2-bootstrap-theme/0.1.0-beta.10/',
        'css': [
            {
                'path': 'select2-bootstrap.min.css',
                'sri': 'sha256-nbyata2PJRjImhByQzik2ot6gSHSU4Cqdz5bNYL2zcU='
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
    },
    'fuse': {
        'url': 'https://cdnjs.cloudflare.com/ajax/libs/fuse.js/3.4.6/',
        'js': [
            {
                'path': 'fuse.min.js',
                'sri': 'sha512-FwWaT/y9ajd/+J06KL9Fko1jELonJNHMUTR4nGP9MSIq4ZdU2w9/OiLxn16p/zEOZkryHi3wKYsnWPuADD328Q=='
            }
        ]
    }
}

# necessary since django 3.2, explicitly set primary key type to avoid warnings
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

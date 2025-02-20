import re

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
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'rdmo.accounts.middleware.TermsAndConditionsRedirectMiddleware'
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
ACCOUNT_TERMS_OF_USE_DATE = None  # None or a valid date string
ACCOUNT_TERMS_OF_USE_EXCLUDE_URL_PREFIXES = ("/admin", "/i18n", "/static", "/account")
ACCOUNT_TERMS_OF_USE_EXCLUDE_URLS = ("/",)  # is LOGOUT_URL needed here?
ACCOUNT_TERMS_OF_USE_EXCLUDE_URL_CONTAINS = []

ACCOUNT_ADAPTER = 'rdmo.accounts.account.AccountAdapter'
ACCOUNT_FORMS = {
    'login': 'rdmo.accounts.account.LoginForm',
    'signup': 'rdmo.accounts.account.SignupForm'
}
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
SOCIALACCOUNT_ADAPTER = 'rdmo.accounts.socialaccount.SocialAccountAdapter'
SOCIALACCOUNT_FORMS = {
    'signup': 'rdmo.accounts.socialaccount.SocialSignupForm'
}
SOCIALACCOUNT_OPENID_CONNECT_URL_PREFIX = ""  # required since 0.60.0 else default is "oidc"

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
    'PROJECT_VISIBILITY',
    'PROJECT_ISSUES',
    'PROJECT_VIEWS',
    'PROJECT_EXPORTS',
    'PROJECT_SNAPSHOT_EXPORTS',
    'PROJECT_IMPORTS',
    'PROJECT_IMPORTS_LIST',
    'PROJECT_SEND_ISSUE',
    'NESTED_PROJECTS',
    'PROJECT_VIEWS_SYNC',
    'PROJECT_TASKS_SYNC'
]

SETTINGS_API = [
    'DEFAULT_URI_PREFIX',
    'LANGUAGES',
    'MULTISITE',
    'GROUPS',
    'EXPORT_FORMATS',
    'PROJECT_TABLE_PAGE_SIZE',
    'PROJECT_CONTACT'
]

TEMPLATES_API = [
    'projects/project_interview_add_set_help.html',
    'projects/project_interview_add_value_help.html',
    'projects/project_interview_buttons_help.html',
    'projects/project_interview_contact_help.html',
    'projects/project_interview_done.html',
    'projects/project_interview_error.html',
    'projects/project_interview_multiple_values_warning.html',
    'projects/project_interview_navigation_help.html',
    'projects/project_interview_overview_help.html',
    'projects/project_interview_page_help.html',
    'projects/project_interview_page_tabs_help.html',
    'projects/project_interview_progress_help.html',
    'projects/project_interview_question_help.html',
    'projects/project_interview_questionset_help.html',
    'projects/project_interview_sidebar.html',
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

EXPORT_MIN_REQUIRED_VERSION = '2.1.0'

PROJECT_TABLE_PAGE_SIZE = 20

PROJECT_VISIBILITY = True

PROJECT_ISSUES = True

PROJECT_ISSUE_PROVIDERS = []

PROJECT_VIEWS = True

PROJECT_CONTACT = False
PROJECT_CONTACT_RECIPIENTS = []

PROJECT_EXPORTS = [
    ('xml', _('RDMO XML'), 'rdmo.projects.exports.RDMOXMLExport'),
    ('csvcomma', _('CSV (comma separated)'), 'rdmo.projects.exports.CSVCommaExport'),
    ('csvsemicolon', _('CSV (semicolon separated)'), 'rdmo.projects.exports.CSVSemicolonExport'),
    ('json', _('JSON'), 'rdmo.projects.exports.JSONExport'),
]

PROJECT_SNAPSHOT_EXPORTS = []

PROJECT_IMPORTS = [
    ('xml', _('RDMO XML'), 'rdmo.projects.imports.RDMOXMLImport'),
]

PROJECT_IMPORTS_LIST = []

PROJECT_FILE_QUOTA = '10Mb'

PROJECT_SEND_ISSUE = False

PROJECT_INVITE_TIMEOUT = None

PROJECT_SEND_INVITE = True

PROJECT_VIEWS_SYNC = False
PROJECT_TASKS_SYNC = False

PROJECT_CREATE_RESTRICTED = False
PROJECT_CREATE_GROUPS = []

PROJECT_VALUES_CONFLICT_THRESHOLD = 0.01

NESTED_PROJECTS = True

OPTIONSET_PROVIDERS = []

PROJECT_VALUES_SEARCH_LIMIT = 10

PROJECT_VALUES_VALIDATION = False

PROJECT_VALUES_VALIDATION_URL = True

PROJECT_VALUES_VALIDATION_INTEGER = True
PROJECT_VALUES_VALIDATION_INTEGER_MESSAGE = _('Enter a valid integer.')
PROJECT_VALUES_VALIDATION_INTEGER_REGEX = re.compile(r'^[+-]?\d+$')

PROJECT_VALUES_VALIDATION_FLOAT = True
PROJECT_VALUES_VALIDATION_FLOAT_MESSAGE = _('Enter a valid float.')
PROJECT_VALUES_VALIDATION_FLOAT_REGEX = re.compile(r'''
    ^[+-]?            # Optional sign
    (
        \d+           # Digits before the decimal or thousands separator
        (,\d{3})*     # Optional groups of exactly three digits preceded by a comma (thousands separator)
        (\.\d+)?      # Optional decimal part, a dot followed by one or more digits
        |             # OR
        \d+           # Digits before the decimal or thousands separator
        (\.\d{3})*    # Optional groups of exactly three digits preceded by a dot (thousands separator)
        (,\d+)?       # Optional decimal part, a comma followed by one or more digits
    )
    ([eE][+-]?\d+)?$  # Optional exponent part
''', re.VERBOSE)

PROJECT_VALUES_VALIDATION_BOOLEAN = True
PROJECT_VALUES_VALIDATION_BOOLEAN_MESSAGE = _('Enter a valid boolean (e.g. 0, 1).')
PROJECT_VALUES_VALIDATION_BOOLEAN_REGEX = r'(?i)^(0|1|f|t|false|true)$'

PROJECT_VALUES_VALIDATION_DATE = True
PROJECT_VALUES_VALIDATION_DATE_MESSAGE = _('Enter a valid date (e.g. "02.03.2024", "03/02/2024", "2024-02-03").')
PROJECT_VALUES_VALIDATION_DATE_REGEX = re.compile(r'''
    ^(
        \d{1,2}\.\s*\d{1,2}\.\s*\d{2,4}  # Format dd.mm.yyyy
        | \d{1,2}/\d{1,2}/\d{4}          # Format mm/dd/yyyy
        | \d{4}-\d{2}-\d{2}              # Format yyyy-mm-dd
    )$
''', re.VERBOSE)

PROJECT_VALUES_VALIDATION_DATETIME = True

PROJECT_VALUES_VALIDATION_EMAIL = True

PROJECT_VALUES_VALIDATION_PHONE = True
PROJECT_VALUES_VALIDATION_PHONE_MESSAGE = _('Enter a valid phone number (e.g. "123456" or "+49 (0) 30 123456").')
PROJECT_VALUES_VALIDATION_PHONE_REGEX = re.compile(r'''
    ^([+]\d{2,3}\s)?  # Optional country code
    (\(\d+\)\s)?      # Optional area code in parentheses
    [\d\s]*$          # Main number with spaces
''', re.VERBOSE)

DEFAULT_URI_PREFIX = 'http://example.com/terms'

REPLACE_MISSING_TRANSLATION = False

# necessary since django 3.2, explicitly set primary key type to avoid warnings
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

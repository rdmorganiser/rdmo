'''
Secret key, use something random in production
'''
#SECRET_KEY = 'this is not a very secret key'

'''
Debug mode, don't use this in production
'''
DEBUG = True

'''
The list of URLs und which this application available
'''
ALLOWED_HOSTS = ['localhost']

'''
Base URL Path to this application, i.e. /path for http://exaple.com/path/
'''
# BASE_URL = '/path'

'''
Additional Django app to be used.
'''
# ADDITIONAL_APPS = (
#    'django_extensions',
#    'allauth.socialaccount.providers.facebook',
#    'allauth.socialaccount.providers.github',
#    'allauth.socialaccount.providers.google',
#    'allauth.socialaccount.providers.orcid',
#    'allauth.socialaccount.providers.twitter',
# )

'''
A directory with a `static` and a `templates` directory containing customisation.
'''
# THEME_DIR = ''

'''
The database connection to be used, see also:
https://docs.djangoproject.com/el/1.10/ref/databases/
'''
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': '',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': '',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': '',
#     }
# }

'''
The main language of this application.
'''
# LANGUAGE_CODE = 'en-us'

'''
The timezone this application.
'''
# TIME_ZONE = 'Europe/Berlin'

'''
Full path for media and static files.
'''
# MEDIA_URL = '/media/'
# STATIC_URL = '/static/'

'''
E-Mail configuration.
'''
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = '25'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = True

'''
LDAP configuration
'''
# import ldap
# from django_auth_ldap.config import LDAPSearch

# AUTH_LDAP_SERVER_URI = "ldap://ldap.example.vbox"
# AUTH_LDAP_BIND_DN = "uid=rdmo,dc=vbox"
# AUTH_LDAP_BIND_PASSWORD = "django"
# AUTH_LDAP_USER_SEARCH = LDAPSearch("cn=users,cn=accounts,dc=example,dc=com", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

# AUTH_LDAP_USER_ATTR_MAP = {
#     "first_name": "givenName",
#     "last_name": "sn",
#     'email': 'mail'
# }

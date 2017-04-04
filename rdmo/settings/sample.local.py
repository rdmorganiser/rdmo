import os
from .base import BASE_DIR, INSTALLED_APPS, AUTHENTICATION_BACKENDS, MIDDLEWARE_CLASSES

'''
Debug mode, don't use this in production
'''
DEBUG = True

'''
Secret key, use something random in production
'''
# SECRET_KEY = 'this is not a very secret key'

'''
The list of URLs und which this application available
'''
ALLOWED_HOSTS = ['localhost']

'''
Base URL Path to this application, i.e. /path for http://exaple.com/path/
'''
# BASE_URL = '/path'

'''
The main language of this application.
'''
# LANGUAGE_CODE = 'en-us'

'''
The timezone this application.
'''
# TIME_ZONE = 'Europe/Berlin'

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
E-Mail configuration.
'''
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = '25'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = False
# EMAIL_USE_SSL = False
# DEFAULT_FROM_EMAIL = ''

'''
Allauth configuration
'''

# ACCOUNT = True
# ACCOUNT_SIGNUP = True
# SOCIALACCOUNT = False
#
# INSTALLED_APPS += [
#     'allauth',
#     'allauth.account',
#     'allauth.socialaccount'
#     'allauth.socialaccount.providers.facebook',
#     'allauth.socialaccount.providers.github',
#     'allauth.socialaccount.providers.google',
#     'allauth.socialaccount.providers.orcid',
#     'allauth.socialaccount.providers.twitter',
# ]
#
# AUTHENTICATION_BACKENDS.append('allauth.account.auth_backends.AuthenticationBackend')

'''
LDAP

Uncomment and edit the following to enable Authentication with a LDAP backend.
'''

# PROFILE_UPDATE = False
#
# import ldap
# from django_auth_ldap.config import LDAPSearch
#
# AUTH_LDAP_SERVER_URI = "ldap://ldap.example.com"
# AUTH_LDAP_BIND_DN = "cn=admin,dc=ldap,dc=example,dc=com"
# AUTH_LDAP_BIND_PASSWORD = "admin"
# AUTH_LDAP_USER_SEARCH = LDAPSearch("dc=ldap,dc=example,dc=com", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
#
# AUTH_LDAP_USER_ATTR_MAP = {
#     "first_name": "givenName",
#     "last_name": "sn",
#     'email': 'mail'
# }
#
# AUTHENTICATION_BACKENDS.insert(
#     AUTHENTICATION_BACKENDS.index('django.contrib.auth.backends.ModelBackend'),
#     'django_auth_ldap.backend.LDAPBackend'
# )

'''
Shibboleth

Uncomment and edit the following to enable Authentication with a Shibboleth service provider.
'''

# SHIBBOLETH = True
# PROFILE_UPDATE = False
#
# INSTALLED_APPS += ['shibboleth']
#
# SHIBBOLETH_ATTRIBUTE_MAP = {
#     'uid': (True, 'username'),
#     'givenName': (True, 'first_name'),
#     'sn': (True, 'last_name'),
#     'mail': (True, 'email'),
# }
#
# AUTHENTICATION_BACKENDS.append('shibboleth.backends.ShibbolethRemoteUserBackend')
#
# MIDDLEWARE_CLASSES.insert(
#     MIDDLEWARE_CLASSES.index('django.contrib.auth.middleware.AuthenticationMiddleware') + 1,
#     'shibboleth.middleware.ShibbolethRemoteUserMiddleware'
# )
#
# LOGIN_URL = '/Shibboleth.sso/Login?target=/projects'
# LOGOUT_URL = '/Shibboleth.sso/Logout'

'''
Theme

A directory with a `static` and a `templates` directory containing customisation.
'''

# THEME_DIR = os.path.join(BASE_DIR, 'theme')

'''
Cache
'''

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#         'KEY_PREFIX': 'rdmo_default'
#     },
#     'api': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#         'KEY_PREFIX': 'rdmo_api'
#     },
# }

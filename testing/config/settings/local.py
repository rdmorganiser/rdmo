import os
from .base import BASE_DIR, INSTALLED_APPS, AUTHENTICATION_BACKENDS, MIDDLEWARE_CLASSES

DEBUG = True

ALLOWED_HOSTS = ['localhost', 'ip6-localhost', '127.0.0.1', '[::1]']

# BASE_URL = '/foo'

# THEME_DIR = os.path.join(BASE_DIR, 'themes/bwFDM-info')

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'rdmo',
#         # 'NAME': 'rdmo_catalog'
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'rdmo',
#         'USER': 'rdmo',
#         'PASSWORD': 'rdmo',
#     }
# }

'''
ALLAUTH
'''

# INSTALLED_APPS += [
#     'allauth',
#     'allauth.account',
#     # 'allauth.socialaccount'
#     # 'allauth.socialaccount.providers.facebook',
#     # 'allauth.socialaccount.providers.github',
#     # 'allauth.socialaccount.providers.google',
#     # 'allauth.socialaccount.providers.orcid',
#     # 'allauth.socialaccount.providers.twitter',
# ]

# ACCOUNT = True
# ACCOUNT_SIGNUP = True
# SOCIALACCOUNT = False

'''
LDAP
'''

# PROFILE_UPDATE = False
#
# import ldap
# from django_auth_ldap.config import LDAPSearch
#
# AUTH_LDAP_SERVER_URI = "ldap://idp.vbox"
# AUTH_LDAP_BIND_DN = "cn=admin,dc=ldap,dc=vbox"
# AUTH_LDAP_BIND_PASSWORD = "admin"
# AUTH_LDAP_USER_SEARCH = LDAPSearch("dc=ldap,dc=vbox", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
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
Cache
'''

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#         'KEY_PREFIX': 'rdmo'
#     },
#     'api': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#         'KEY_PREFIX': 'rdmo_api'
#     }
# }

'''
Logging
'''

# LOGGING = {
#     'disable_existing_loggers': False,
#     'version': 1,
#     'handlers': {
#         'sql': {
#             'class': 'logging.FileHandler',
#             'level': 'DEBUG',
#             'filename': '/var/log/django/sql.log',
#         },
#         'rules': {
#             'class': 'logging.FileHandler',
#             'level': 'DEBUG',
#             'filename': '/var/log/django/rules.log',
#         },
#         'ldap': {
#             'class': 'logging.FileHandler',
#             'level': 'DEBUG',
#             'filename': '/var/log/django/ldap.log',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['sql'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#         'rules': {
#             'handlers': ['rules'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django_auth_ldap': {
#             'handlers': ['ldap'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#     },
# }

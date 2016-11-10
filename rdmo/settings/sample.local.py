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
# DEVELOPMENT_APPS = (
#    'django_extensions',
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

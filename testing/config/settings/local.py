DEBUG = True

SECRET_KEY = 'this is a not very secret key'

ALLOWED_HOSTS = ['localhost', 'ip6-localhost', '127.0.0.1', '[::1]']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rdmo'
    }
}

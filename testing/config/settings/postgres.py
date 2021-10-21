DEBUG = True

SECRET_KEY = 'this is a not very secret key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rdmo',
        'USER': 'postgres',
        'PASSWORD': 'postgres_password',
        'HOST': '127.0.0.1',
    }
}

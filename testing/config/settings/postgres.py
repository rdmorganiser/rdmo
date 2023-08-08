DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rdmo',
        'USER': 'postgres_user',
        'PASSWORD': 'postgres_password',
        'HOST': '127.0.0.1',
        'TEST': {'SERIALIZE': False},
    }
}

DEBUG = True

SECRET_KEY = 'this is a not very secret key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rdmo',
        'USER': 'root',
        'PASSWORD': '',
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
        },
        'OPTIONS': {
            'init_command': "SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));"
        }
    }
}

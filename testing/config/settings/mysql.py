DEBUG = True

SECRET_KEY = 'this is a not very secret key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rdmo',
        'USER': 'root',
        'PASSWORD': ''
    }
}

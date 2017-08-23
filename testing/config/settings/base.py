import os

from . import INSTALLED_APPS

SITE_ID = 1

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components_root')

FIXTURE_DIRS = (
   os.path.join(BASE_DIR, 'fixtures'),
)

INSTALLED_APPS += [
    'allauth',
    'allauth.account'
]

ACCOUNT = True
ACCOUNT_SIGNUP = True
SOCIALACCOUNT = False

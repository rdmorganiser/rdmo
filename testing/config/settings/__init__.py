from pathlib import Path

from split_settings.tools import include, optional

from rdmo.core.settings import *  # import all rdmo default settings
from rdmo.core.utils import sanitize_url

BASE_DIR = Path(__file__).parent.parent.parent
MEDIA_ROOT = BASE_DIR / 'media_root'
STATIC_ROOT = BASE_DIR / 'static_root'
STATICFILES_DIRS = [BASE_DIR / 'vendor']

include(
    optional('base.py'),
    optional('local.py')
)

# prepend the BASE_URL to the different URL settings
try:
    BASE_URL = sanitize_url(BASE_URL)
    LOGIN_URL = sanitize_url(BASE_URL + LOGIN_URL)
    LOGIN_REDIRECT_URL = sanitize_url(BASE_URL + LOGIN_REDIRECT_URL)
    LOGOUT_URL = sanitize_url(BASE_URL + LOGOUT_URL)
    MEDIA_URL = sanitize_url(BASE_URL + MEDIA_URL)
    STATIC_URL = sanitize_url(BASE_URL + STATIC_URL)

    ACCOUNT_LOGOUT_REDIRECT_URL = BASE_URL
    CSRF_COOKIE_PATH = BASE_URL
    LANGUAGE_COOKIE_PATH = BASE_URL
    SESSION_COOKIE_PATH = BASE_URL
except NameError:
    pass

from rdmo.core.settings import *

from .base import *
from .local import *

# add static and templates from local.THEME_DIR to STATICFILES_DIRS and TEMPLATES
try:
    STATICFILES_DIRS = [
        os.path.join(THEME_DIR, 'static/')
    ]
    TEMPLATES[0]['DIRS'].append(os.path.join(THEME_DIR, 'templates/'))
except NameError:
    pass

# prepend the local.BASE_URL to the different URL settings
try:
    LOGIN_URL = BASE_URL + LOGIN_URL
    LOGIN_REDIRECT_URL = BASE_URL + LOGIN_REDIRECT_URL
    LOGOUT_URL = BASE_URL + LOGOUT_URL
    ACCOUNT_LOGOUT_REDIRECT_URL = BASE_URL
    MEDIA_URL = BASE_URL + MEDIA_URL
    STATIC_URL = BASE_URL + STATIC_URL

    CSRF_COOKIE_PATH = BASE_URL + '/'
    LANGUAGE_COOKIE_PATH = BASE_URL + '/'
    SESSION_COOKIE_PATH = BASE_URL + '/'
except NameError:
    pass

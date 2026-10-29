import sys
from importlib import import_module, reload

from django.urls import clear_url_caches, get_resolver


def reload_urlconf(urlconf=None, root_urlconf=None):
    clear_url_caches()
    if urlconf is None and root_urlconf is None:
        from django.conf import settings
        urlconf = settings.ROOT_URLCONF
    elif urlconf is None and root_urlconf is not None:
        # take the settings during pytest run
        urlconf = root_urlconf

    if urlconf in sys.modules:
        reload(sys.modules[urlconf])
    else:
        import_module(urlconf)


def reload_urls(*app_names: str, root_urlconf=None) -> None:
    # reload the urlconf of the app
    for _app in app_names:
        reload_urlconf(urlconf=_app)

    # reload the core urlconf
    reload_urlconf(urlconf='rdmo.core.urls')

    # reload the testcase settings urlconf
    reload_urlconf(root_urlconf=root_urlconf)

    get_resolver()._populate()

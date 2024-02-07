import sys
from importlib import import_module, reload
from typing import Optional

from django.urls import clear_url_caches


def reload_urlconf(urlconf=None, settings=None):
    clear_url_caches()

    if urlconf is None and settings is None:
        from django.conf import settings
        urlconf = settings.ROOT_URLCONF
    elif urlconf is None and settings is not None:
        # take the settings during pytest run
        urlconf = settings.ROOT_URLCONF

    if urlconf in sys.modules:
        reload(sys.modules[urlconf])
    else:
        import_module(urlconf)


def reload_urls(app_name: Optional[str] = None, settings=None) -> None:
    # reload the urlconf of the app
    if app_name is not None:
        reload_urlconf(urlconf=f'rdmo.{app_name}.urls', settings=settings)

    # reload the core urlconf
    reload_urlconf(urlconf='rdmo.core.urls', settings=settings)

    # reload the testcase settings urlconf
    reload_urlconf(settings=settings)

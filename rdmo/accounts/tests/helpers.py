import sys
from importlib import import_module, reload

import pytest

from django.urls import clear_url_caches, get_resolver, reverse


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


def reload_urls(*app_names: str, root_urlconf = None) -> None:
    # reload the urlconf of the app
    for _app in app_names:
        reload_urlconf(urlconf=_app)

    # reload the core urlconf
    reload_urlconf(urlconf='rdmo.core.urls')

    # reload the testcase settings urlconf
    reload_urlconf(root_urlconf=root_urlconf)

    get_resolver()._populate()


@pytest.fixture
def enable_terms_of_use(settings):  # noqa: PT004
    settings.ACCOUNT_TERMS_OF_USE = True
    settings.MIDDLEWARE += [
        settings.ACCOUNT_TERMS_OF_USE_MIDDLEWARE
    ]
    reload_urls('rdmo.accounts.urls')

    yield

    # revert settings to initial state
    settings.ACCOUNT_TERMS_OF_USE = False
    settings.MIDDLEWARE.remove(settings.ACCOUNT_TERMS_OF_USE_MIDDLEWARE)
    # 🔹 Reload URLs to reflect the changes
    reload_urls('rdmo.accounts.urls')


@pytest.fixture
def enable_socialaccount(settings):  # noqa: PT004
    # Arrange: this fixture enable and initializes the allauth.sociallaccount
    # INSTALLED_APPS already has "allauth.socialaccount","allauth.socialaccount.providers.dummy"
    settings.SOCIALACCOUNT = True
    settings.SOCIALACCOUNT_SIGNUP = True

    assert reverse("dummy_login")  # Ensure the route exists

    yield  # Run test

    # 🔹 Cleanup: reset settings
    settings.SOCIALACCOUNT = False
    settings.SOCIALACCOUNT_SIGNUP = False

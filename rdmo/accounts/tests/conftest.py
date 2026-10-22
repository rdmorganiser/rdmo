import sys
import types

import pytest

from django.urls import reverse

from .helpers import reload_urls


@pytest.fixture
def enable_terms_of_use(settings):
    settings.ACCOUNT_TERMS_OF_USE = True
    reload_urls('rdmo.accounts.urls')

    yield

    # revert settings to initial state
    settings.ACCOUNT_TERMS_OF_USE = False
    # 🔹 Reload URLs to reflect the changes
    reload_urls('rdmo.accounts.urls')


@pytest.fixture
def enable_socialaccount(settings):
    # Arrange: this fixture enable and initializes the allauth.sociallaccount
    # INSTALLED_APPS already has "allauth.socialaccount","allauth.socialaccount.providers.dummy"
    settings.SOCIALACCOUNT = True
    settings.SOCIALACCOUNT_SIGNUP = True

    assert reverse("dummy_login")  # Ensure the route exists

    yield  # Run test

    # 🔹 Cleanup: reset settings
    settings.SOCIALACCOUNT = False
    settings.SOCIALACCOUNT_SIGNUP = False


@pytest.fixture
def enable_shibboleth(settings):
    """Mark the instance as using Shibboleth without touching INSTALLED_APPS."""
    settings.SHIBBOLETH = True
    try:
        yield
    finally:
        settings.SHIBBOLETH = False


@pytest.fixture
def fake_shibboleth(monkeypatch):
    """Factory fixture: returns a function to (re)create a fake 'shibboleth'
    package with a configurable app_settings object. Cleans up automatically.
    """
    created = []

    def _make(*, has_unquote: bool) -> None:
        mod = types.ModuleType('shibboleth')
        app_settings = types.SimpleNamespace()
        if has_unquote:
            # Mimic the RDMO/unquoted-aware builds
            app_settings.UNQUOTE_ATTRIBUTES = False
        mod.app_settings = app_settings
        monkeypatch.setitem(sys.modules, 'shibboleth', mod)
        created.append('shibboleth')

    yield _make

    # 🔹 Cleanup injected modules
    for name in created:
        sys.modules.pop(name, None)

import os

import pytest

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client

from playwright.sync_api import Page

from rdmo.accounts.utils import set_group_permissions

USERNAME = "editor"  # the user needs exist in the database
PLAYWRIGHT_TIMEOUT = 10_000  # timeout in ms


@pytest.fixture(scope="session", autouse=True)
def _set_django_allow_async_unsafe():
    """pytest-playwright needs this setting to be enabled."""
    os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
def django_db_setup(django_db_setup, django_db_blocker, fixtures): # noqa: PT004 - pytest-django requires this name "django_db_setup"
    """Set up database and populate with fixtures, that get restored for every test case.

    This fixture overrides the django_db_setup in the main conftest.py, this only applies to the e2e tests
    in this directory.
    """
    with django_db_blocker.unblock():
        call_command("loaddata", *fixtures, verbosity=0)
        set_group_permissions()


@pytest.fixture
def authenticated_client(db) -> Client:
    """An authenticated test client, used to bypass the login page."""
    user = get_user_model().objects.get(username=USERNAME)
    client = Client()
    client.user = user  # attach user to client to access in other fixtures
    client.force_login(user)
    return client


@pytest.fixture
def page(live_server, browser, authenticated_client) -> Page:
    """An authenticated playwright page.

    The page is authenticated with session cookies from authenticated_client.
    The page has access to the live server and starts at "/management".
    The page has the authenticated user attached to it.
    """

    # retrieve the session cookie from the authenticated client
    session_cookie = authenticated_client.cookies[settings.SESSION_COOKIE_NAME]
    cookie = {
        "name": session_cookie.key,
        "value": session_cookie.value,
        "url": live_server.url,
    }
    context = browser.new_context(base_url=live_server.url)
    # the browser context is now "authenticated" with the session cookie
    context.add_cookies([cookie])
    page = context.new_page()
    page.set_default_timeout(PLAYWRIGHT_TIMEOUT)
    page.set_default_navigation_timeout(PLAYWRIGHT_TIMEOUT)
    page.user = authenticated_client.user  # attach user to page to access in tests
    # the page starts at base_url + /management
    page.goto("/management")
    yield page
    context.close()

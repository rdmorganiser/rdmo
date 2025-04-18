import os

import pytest

from django.conf import settings
from django.core.management import call_command

from playwright.sync_api import Browser, BrowserContext, Page

from rdmo.accounts.utils import set_group_permissions

PLAYWRIGHT_TIMEOUT = 10_000  # timeout in ms

@pytest.fixture(scope="session", autouse=True)
def _set_django_allow_async_unsafe():
    """pytest-playwright needs this setting to be enabled."""
    os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
def django_db_setup(django_db_setup, django_db_blocker, fixtures):
    """Set up database and populate with fixtures, that get restored for every test case.

    This fixture overrides the django_db_setup in the main conftest.py, this only applies to the e2e tests
    in this directory.
    """
    with django_db_blocker.unblock():
        call_command("loaddata", *fixtures, verbosity=0)
        set_group_permissions()


@pytest.fixture
def authenticated_context(client, login, live_server, browser: Browser, e2e_username) -> BrowserContext:
    """Creates an authenticated Playwright browser context with session cookies."""
    # retrieve the session cookie from the authenticated client
    login(e2e_username)
    session_cookie = client.cookies[settings.SESSION_COOKIE_NAME]
    cookie = {
        "name": session_cookie.key,
        "value": session_cookie.value,
        "url": live_server.url,
    }

    context = browser.new_context(base_url=live_server.url)
    # the browser context is now "authenticated" with the session cookie
    context.add_cookies([cookie])
    yield context
    context.close()


@pytest.fixture
def authenticated_page(authenticated_context: BrowserContext) -> Page:
    """Provides an authenticated Playwright page without forcing navigation.
    The page is authenticated with session cookies from authenticated_context.
    """
    page = authenticated_context.new_page()
    page.set_default_timeout(PLAYWRIGHT_TIMEOUT)
    page.set_default_navigation_timeout(PLAYWRIGHT_TIMEOUT)
    yield page
    page.close()


@pytest.fixture(autouse=True)
def fail_on_js_error(page: Page):
    """Fail the test immediately when a JavaScript error occurs."""

    # List of ignored warning substrings
    ignored_warnings = [
        "legacy childContextTypes API",
        "legacy contextTypes API",
        "Use React.createContext()",
    ]

    def log_console_msg(msg):
        if msg.type == "error":
            # Check if the message contains any ignored warning
            if any(ignored in msg.text for ignored in ignored_warnings):
                print(f"Ignoring warning: {msg.text}")  # Log it for visibility but don't fail
                return
            pytest.fail(f"JavaScript error detected: {msg.text}")

    def log_page_error(exception):
        pytest.exit(f"Uncaught page error detected: {exception}")

    page.on("console", log_console_msg)
    page.on("pageerror", log_page_error)

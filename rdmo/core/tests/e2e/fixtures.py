import os
from urllib.parse import urlparse

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


@pytest.fixture(autouse=True)
def allow_live_server_host(settings, live_server):
    """Allow the pytest live server host in Django host validation."""
    hosts = {
        *settings.ALLOWED_HOSTS,
        urlparse(live_server.url).hostname,
        "localhost",
        "127.0.0.1",
        "testserver",
    }
    settings.ALLOWED_HOSTS = list(hosts)


@pytest.fixture
def django_db_setup(django_db_setup, django_db_blocker, fixtures):
    """Set up database and populate it with fixtures for every e2e test."""
    with django_db_blocker.unblock():
        call_command("loaddata", *fixtures, verbosity=0)
        set_group_permissions()


@pytest.fixture
def authenticated_context(client, login, live_server, browser: Browser, e2e_username) -> BrowserContext:
    """Create an authenticated Playwright browser context."""
    login(e2e_username)
    session_cookie = client.cookies[settings.SESSION_COOKIE_NAME]
    cookie = {
        "name": session_cookie.key,
        "value": session_cookie.value,
        "url": live_server.url,
    }

    context = browser.new_context(base_url=live_server.url)
    context.add_cookies([cookie])
    try:
        yield context
    finally:
        context.close()


@pytest.fixture
def authenticated_page(authenticated_context: BrowserContext) -> Page:
    """Create an authenticated Playwright page and collect JS errors."""
    js_errors = []
    ignored_warnings = [
        "legacy childContextTypes API",
        "legacy contextTypes API",
        "Use React.createContext()",
    ]

    def log_console_msg(msg):
        if msg.type == "error":
            if any(ignored in msg.text for ignored in ignored_warnings):
                print(f"Ignoring warning: {msg.text}")
                return
            js_errors.append(f"console error: {msg.text}")

    def log_page_error(exception):
        js_errors.append(f"page error: {exception}")

    page = authenticated_context.new_page()
    page.set_default_timeout(PLAYWRIGHT_TIMEOUT)
    page.set_default_navigation_timeout(PLAYWRIGHT_TIMEOUT)
    page.on("console", log_console_msg)
    page.on("pageerror", log_page_error)
    try:
        yield page
    finally:
        page.close()
        if js_errors:
            pytest.fail("\n".join(js_errors))

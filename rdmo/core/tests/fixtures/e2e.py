import os
from urllib.parse import urlparse

import pytest

from django.conf import settings
from django.core.management import call_command

from playwright.sync_api import Browser, BrowserContext, Page

from rdmo.accounts.utils import set_group_permissions

PLAYWRIGHT_TIMEOUT = 10_000  # timeout in ms


def pytest_runtest_setup(item):
    """pytest-playwright needs this setting to be enabled, before any fixture of an e2e test is set up."""
    if item.get_closest_marker("e2e"):
        os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
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
def e2e_db(transactional_db, django_db_blocker, fixtures):
    """Populate the database with fixtures for every e2e test, since transactional_db flushes it afterwards."""
    with django_db_blocker.unblock():
        call_command("loaddata", *fixtures, verbosity=0)
        call_command("rebuild_mptt")
        set_group_permissions()


@pytest.fixture
def authenticated_context(
    e2e_db, allow_live_server_host, client, login, live_server, browser: Browser, e2e_username
) -> BrowserContext:
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

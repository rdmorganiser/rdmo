import pytest

from playwright.sync_api import Page

from rdmo.core.tests.e2e.conftest import (  # noqa: F401
    PLAYWRIGHT_TIMEOUT,
    _set_django_allow_async_unsafe,
    authenticated_context,
    authenticated_page,
    django_db_setup,
    fail_on_js_error,
)


@pytest.fixture
def e2e_username(scope="session") -> str:
    """Fixture to specify which user should be authenticated.
    This can be overridden in individual test modules or fixtures.
    """
    return "editor"


@pytest.fixture
def page(django_db_setup, live_server, browser, authenticated_page: Page) -> Page:  # noqa: F811
    """Navigates the authenticated page to /management."""
    authenticated_page.goto("/management")  # Navigate to the projects section
    authenticated_page.wait_for_load_state()  # maybe not needed
    return authenticated_page


@pytest.fixture
def page_multisite(django_db_setup, live_server, browser, authenticated_page: Page, settings) -> Page:  # noqa: F811
    """Enables the multisite and navigates the authenticated page to /management."""
    settings.MULTISITE = True
    authenticated_page.goto("/management")  # Navigate to the projects section
    authenticated_page.wait_for_load_state()  # maybe not needed
    return authenticated_page

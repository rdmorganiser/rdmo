
import pytest

from playwright.sync_api import Page, expect

from rdmo.core.tests.e2e.fixtures import (  # noqa: F401
    PLAYWRIGHT_TIMEOUT,
    _set_django_allow_async_unsafe,
    allow_live_server_host,
    authenticated_context,
    authenticated_page,
    django_db_setup,
)


@pytest.fixture
def e2e_username() -> str:
    """Fixture to specify which user should be authenticated.
    This can be overridden in individual test modules or fixtures.
    """
    return "owner"


@pytest.fixture
def page(live_server, browser, authenticated_page: Page) -> Page: # noqa: F811
    """Navigates the authenticated page to /projects."""
    authenticated_page.goto("/projects")  # Navigate to the projects section
    expect(authenticated_page).to_have_url("/projects/")
    return authenticated_page

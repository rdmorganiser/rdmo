
import pytest

from playwright.sync_api import Page

from rdmo.core.tests.e2e.conftest import (  # noqa: F401
    PLAYWRIGHT_TIMEOUT,
    _set_django_allow_async_unsafe,
    authenticated_client,
    authenticated_context,
    authenticated_page,
    django_db_setup,
)

USERNAME = "owner"


@pytest.fixture
def e2e_username() -> str:
    """Fixture to specify which user should be authenticated.
    This can be overridden in individual test modules or fixtures.
    """
    return USERNAME


@pytest.fixture
def page(live_server, browser, authenticated_page: Page) -> Page: # noqa: F811
    """Navigates the authenticated page to /projects."""
    authenticated_page.goto("/projects")  # Navigate to the projects section
    authenticated_page.wait_for_load_state("networkidle")
    return authenticated_page

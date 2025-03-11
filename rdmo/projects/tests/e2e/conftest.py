
import pytest

from playwright.sync_api import Page

USERNAME = "owner"  # the user needs exist in the database


@pytest.fixture
def e2e_username() -> str:
    """Fixture to specify which user should be authenticated.
    This can be overridden in individual test modules or fixtures.
    """
    return USERNAME


@pytest.fixture
def page(live_server, browser, authenticated_page: Page) -> Page:
    """Navigates the authenticated page to /projects."""
    page = authenticated_page
    page.goto("/projects")  # Navigate to the projects section
    return page

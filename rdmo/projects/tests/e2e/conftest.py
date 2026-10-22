import pytest

from playwright.sync_api import Page, expect


@pytest.fixture
def e2e_username() -> str:
    """Fixture to specify which user should be authenticated.
    This can be overridden in individual test modules or fixtures.
    """
    return "owner"


@pytest.fixture
def page(live_server, browser, authenticated_page: Page) -> Page:
    """Navigates the authenticated page to /projects."""
    authenticated_page.goto("/projects")  # Navigate to the projects section
    expect(authenticated_page).to_have_url("/projects/")
    return authenticated_page

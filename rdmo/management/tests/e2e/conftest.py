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


@pytest.fixture(scope="session")
def e2e_username() -> str:
    """Fixture to specify which user should be authenticated.
    This can be overridden in individual test modules or fixtures.
    """
    return "editor"


@pytest.fixture
def page_single(transactional_db, live_server, authenticated_page: Page) -> Page:  # noqa: F811
    """Navigates the authenticated page to /management."""
    authenticated_page.goto("/management")  # Navigate to the projects section
    expect(authenticated_page.get_by_role("heading", name="Management")).to_be_visible()
    return authenticated_page


@pytest.fixture
def page_multisite(transactional_db, live_server, authenticated_page: Page, settings) -> Page:  # noqa: F811
    """Enables the multisite and navigates the authenticated page to /management."""
    settings.MULTISITE = True
    authenticated_page.goto("/management")  # Navigate to the projects section
    expect(authenticated_page.get_by_role("heading", name="Management")).to_be_visible()
    return authenticated_page


@pytest.fixture
def page(request, transactional_db) -> Page:
    """Allow specific page fixtures to be selected indirectly and default to multisite."""
    fixture_name = getattr(request, "param", "page_multisite")
    return request.getfixturevalue(fixture_name)

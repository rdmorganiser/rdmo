import pytest

from playwright.sync_api import Page

from rdmo.core.tests.e2e.conftest import (  # noqa: F401
    PLAYWRIGHT_TIMEOUT,
    _set_django_allow_async_unsafe,
    authenticated_client,
    authenticated_context,
    authenticated_page,
    django_db_setup,
    enable_multisite,
    fail_on_js_error,
)
from rdmo.management.tests.helpers_models import delete_all_objects
from rdmo.options.models import Option, OptionSet
from rdmo.questions.models import Catalog, Question, Section
from rdmo.questions.models import Page as PageModel
from rdmo.questions.models.questionset import QuestionSet


@pytest.fixture
def e2e_username(scope="session") -> str:
    """Fixture to specify which user should be authenticated.
    This can be overridden in individual test modules or fixtures.
    """
    return "editor"  # the user needs to exist in the database


@pytest.fixture
def page(django_db_setup, live_server, browser, authenticated_page: Page, enable_multisite) -> Page:  # noqa: F811
    """Navigates the authenticated page to /management."""
    authenticated_page.goto("/management")  # Navigate to the projects section
    authenticated_page.wait_for_load_state()  # maybe not needed
    return authenticated_page

@pytest.fixture
def delete_catalog_objects(django_db_blocker):
    with django_db_blocker.unblock():
        delete_all_objects([Catalog, Section, PageModel, QuestionSet, Question])


@pytest.fixture
def delete_option_objects(django_db_blocker):
    with django_db_blocker.unblock():
        delete_all_objects([OptionSet, Option])

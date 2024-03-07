# ruff: noqa: F811
import os

import pytest

from playwright.sync_api import Page, expect

from rdmo.questions.models import Catalog, Question, Section
from rdmo.questions.models import Page as PageModel
from rdmo.questions.models.questionset import QuestionSet

from .helpers_models import delete_all_objects

pytestmark = pytest.mark.e2e

# needed for playwright to run
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

test_users = [('editor', 'editor')]

@pytest.mark.parametrize("username, password", test_users)  # consumed by fixture
def test_import_catalogs_in_management(logged_in_user: Page) -> None:
    """Test that the catalogs.xml can be imported correctly."""
    delete_all_objects([Catalog, Section, PageModel, QuestionSet, Question])

    page = logged_in_user
    expect(page.get_by_role("heading", name="Management")).to_be_visible()
    expect(page.locator("strong").filter(has_text="Catalogs")).to_be_visible()
    # choose the file to be imported
    page.locator("input[name=\"uploaded_file\"]").set_input_files("./testing/xml/elements/catalogs.xml")
    # click the import form submit button, this will take some time
    page.locator('#sidebar div.elements-sidebar form.upload-form.sidebar-form div.sidebar-form-button button.btn.btn-primary').click()  # noqa: E501
    # wait for import to be finished with timeout 30s
    expect(page.get_by_text("Import from: catalogs.xml")).to_be_visible(timeout=30_000)
    ## TODO test if ImportInfo numbers are correct
    # test the components of the import-before-import staging page
    page.locator(".element-link").first.click()
    page.get_by_role("link", name="Unselect all").click()
    page.get_by_role("link", name="Select all", exact=True).click()
    page.get_by_role("link", name="Show all").click()
    rows_displayed_in_ui = page.locator(".list-group > .list-group-item > .row.mt-10")
    expect(rows_displayed_in_ui).to_have_count(148)
    page.get_by_role("link", name="Hide all").click()
    expect(rows_displayed_in_ui).to_have_count(0)
    page.screenshot(path="screenshots/management-import-pre-import.png", full_page=True)
    # click the import button to start saving the instances to the db
    page.get_by_role("button", name="Import 148 elements").click()
    expect(page.get_by_role("heading", name="Import successful")).to_be_visible()
    page.screenshot(path="screenshots/management-import-post-import.png", full_page=True)
    page.get_by_text("Created:").click()
    # go back to management page
    page.get_by_role("button", name="Back").click()
    expect(page.get_by_role("heading", name="Management")).to_be_visible()
    # assert all Model objects in db
    assert Catalog.objects.count() == 2
    assert Section.objects.count() == 6
    assert PageModel.objects.count() == 48
    assert QuestionSet.objects.count() == 3
    assert Question.objects.count() == 89

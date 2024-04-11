# ruff: noqa: F811
import os

import pytest

from playwright.sync_api import Page, expect

from rdmo.options.models import Option, OptionSet

from .helpers_models import delete_all_objects

pytestmark = pytest.mark.e2e

# needed for playwright to run
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

test_users = [('editor', 'editor')]
import_xml = "./testing/xml/elements/optionsets.xml"
import_xml_1 = "./testing/xml/elements/updated-and-changed/optionsets-1.xml"
OPTIONS_TOTAL_COUNT = 13

@pytest.mark.parametrize("username, password", test_users)  # consumed by fixture
def test_import_and_update_optionsets_in_management(logged_in_user: Page) -> None:
    """Test that each content type is available through the navigation."""
    delete_all_objects([OptionSet, Option])

    page = logged_in_user
    expect(page.get_by_role("heading", name="Management")).to_be_visible()
    expect(page.locator("strong").filter(has_text="Catalogs")).to_be_visible()
    ## 1. Import fresh optionset.xml
    # choose the file to be imported
    page.locator("input[name=\"uploaded_file\"]").set_input_files(import_xml)
    # click the import form submit button, this will take some time
    page.locator('#sidebar div.elements-sidebar form.upload-form.sidebar-form div.sidebar-form-button button.btn.btn-primary').click()  # noqa: E501
    # wait for import to be finished with timeout 30s
    expect(page.get_by_text("Import from: optionsets.xml")).to_be_visible(timeout=30_000)
    ## TODO test if ImportInfo numbers are correct
    # test the components of the import-before-import staging page
    expect(page.get_by_text(f"Created: {OPTIONS_TOTAL_COUNT}")).to_be_visible(timeout=30_000)
    page.locator(".element-link").first.click()
    page.get_by_role("link", name="Unselect all").click()
    page.get_by_role("link", name="Select all", exact=True).click()
    page.get_by_role("link", name="Show all", exact=True).click()
    rows_displayed_in_ui = page.locator(".list-group > .list-group-item > .row.mt-10")
    expect(rows_displayed_in_ui).to_have_count(OPTIONS_TOTAL_COUNT)
    # click the import button to start saving the instances to the db
    page.get_by_role("button", name=f"Import {OPTIONS_TOTAL_COUNT} elements").click()
    expect(page.get_by_role("heading", name="Import successful")).to_be_visible()
    page.screenshot(path="screenshots/management-import-optionsets-post-import.png", full_page=True)
    page.get_by_text("Created:").click()
    # go back to management page
    page.get_by_role("button", name="Back").click()
    expect(page.get_by_role("heading", name="Management")).to_be_visible()
    # assert all Model objects in db
    assert OptionSet.objects.count() == 4
    assert Option.objects.count() == 9

    ## 2. import optionset-1.xml with changes
    # choose the file to be imported
    page.locator("input[name=\"uploaded_file\"]").set_input_files(import_xml_1)
    # click the import form submit button, this will take some time
    page.locator('#sidebar div.elements-sidebar form.upload-form.sidebar-form div.sidebar-form-button button.btn.btn-primary').click()  # noqa: E501
    expect(page.get_by_text("Import from: optionsets-1.xml")).to_be_visible(timeout=40_000)
    # assert changed elements
    expect(page.get_by_text(f"Total: {OPTIONS_TOTAL_COUNT} Updated: {OPTIONS_TOTAL_COUNT} (Changed: 5) Warnings: 1")).to_be_visible(timeout=30_000)  # noqa: E501
    expect(page.get_by_text("Filter changed (5)")).to_be_visible()
    page.get_by_text("Filter changed (5)").click()
    page.get_by_role("link", name="Show changes").click()
    expect(page.get_by_text("http://example.com/terms/options/one_two_three/three").nth(1)).to_be_visible()
    page.screenshot(path="screenshots/management-import-optionsets-1-changes.png", full_page=True)
    ## TODO test for warnings, errors

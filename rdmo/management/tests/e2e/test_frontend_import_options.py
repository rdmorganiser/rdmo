import pytest

from playwright.sync_api import Page, expect

from rdmo.management.tests.e2e.frontend_helpers import assert_warning_items
from rdmo.management.tests.helpers_import_elements import IMPORT_ELEMENT_PANELS_LOCATOR
from rdmo.options.models import Option, OptionSet

pytestmark = pytest.mark.e2e

import_xml = "./testing/xml/elements/optionsets.xml"
import_xml_1 = "./testing/xml/elements/updated-and-changed/optionsets-1.xml"
OPTIONSETS_COUNTS = {"total": 13, "updated": 13, "changed": 5, "warnings": 2}
OPTIONSETS_COUNTS_HEADER_INFOS = [f"{k.capitalize()}: {v}" for k, v in OPTIONSETS_COUNTS.items()]
# Defined in filterCheckBoxText in rdmo/management/assets/js/components/import/common/ImportFilters.js
IMPORT_FILTER_LABEL_TEXT = 'Show only new and changed elements (%s)'


def test_import_and_update_optionsets_in_management(db, page: Page, delete_all_objects) -> None:
    """Test that each content type is available through the navigation."""

    expect(page.get_by_role("heading", name="Management")).to_be_visible()
    expect(page.locator("strong").filter(has_text="Catalogs")).to_be_visible()
    # delete the OptionSet, Option objects
    delete_all_objects(OptionSet, Option)

    ## 1. Import fresh optionset.xml
    # choose the file to be imported
    page.locator('input[name="uploaded_file"]').set_input_files(import_xml)
    # click the import form submit button, this will take some time
    page.locator(
        "#sidebar div.elements-sidebar form.upload-form.sidebar-form div.sidebar-form-button button.btn.btn-primary"
    ).click()
    # wait for import to be finished with timeout 30s
    expect(page.get_by_text("Import from: optionsets.xml")).to_be_visible(timeout=30_000)
    ## TODO test if ImportInfo numbers are correct
    # test the components of the import-before-import staging page
    expect(page.get_by_text(f"Created: {OPTIONSETS_COUNTS['total']}")).to_be_visible(timeout=30_000)
    page.locator(".element-link").first.click()
    page.get_by_role("link", name="Deselect all").click()
    page.get_by_role("link", name="Select all", exact=True).click()
    page.get_by_role("link", name="Show all", exact=True).click()
    rows_displayed_in_ui = page.locator(IMPORT_ELEMENT_PANELS_LOCATOR)
    expect(rows_displayed_in_ui).to_have_count(OPTIONSETS_COUNTS["total"])
    # click the import button to start saving the instances to the db
    page.get_by_role("button", name=f"Import {OPTIONSETS_COUNTS['total']} elements").click()
    expect(page.get_by_role("heading", name="Import successful")).to_be_visible()
    page.screenshot(path="screenshots/management/import-optionsets-post-import.png", full_page=True)
    page.get_by_text("Created:").click()
    # go back to management page
    page.get_by_role("button", name="Back").click()
    expect(page.get_by_role("heading", name="Management")).to_be_visible()
    # assert all Model objects in db
    assert OptionSet.objects.count() == 4
    assert Option.objects.count() == 9

    ## 2. import optionset-1.xml with changes
    # choose the file to be imported
    page.locator('input[name="uploaded_file"]').set_input_files(import_xml_1)
    # click the import form submit button, this will take some time
    page.locator(
        "#sidebar div.elements-sidebar form.upload-form.sidebar-form div.sidebar-form-button button.btn.btn-primary"
    ).click()
    expect(page.get_by_text("Import from: optionsets-1.xml")).to_be_visible(timeout=40_000)
    # assert changed elements
    for text in OPTIONSETS_COUNTS_HEADER_INFOS:
        expect(page.locator("#main")).to_contain_text(text)
    expect(page.get_by_text(IMPORT_FILTER_LABEL_TEXT % OPTIONSETS_COUNTS['changed'])).to_be_visible()
    page.get_by_role("link", name="Show changes").click()
    expect(page.locator(".col-sm-6 > .form-group").first).to_be_visible(timeout=30_000)
    # take a screenshot of the import page
    expect(page.get_by_text("http://example.com/terms/options/one_two_three/three").nth(1)).to_be_visible()

    # test for Warnings
    expected_warnings = [
        (
            "Option set ",
            "http://example.com/terms/options/condition",
            "Condition http://example.com/terms/conditions/optionset_bool_is_false for OptionSet http://example.com/terms/options/condition does not exist.",  # noqa: E501
        ),
        (
            "Option set ",
            "http://example.com/terms/options/one_two_three",
            "Condition http://example.com/terms/conditions/does_not_exist for OptionSet http://example.com/terms/options/one_two_three does not exist.",  # noqa: E501
        ),
    ]
    assert_warning_items(page, expected_warnings)

    ## TODO add test for errors

    page.locator("body").press("Home")
    expect(page.get_by_role("link", name="Management", exact=True)).to_be_visible()
    page.screenshot(path="screenshots/management/import-optionsets-1-changes.png", full_page=True)

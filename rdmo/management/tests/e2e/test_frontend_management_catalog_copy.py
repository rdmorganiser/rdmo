# ruff: noqa: F811
import pytest

from playwright.sync_api import Page, expect

from rdmo.questions.models import Catalog

pytestmark = pytest.mark.e2e


@pytest.mark.parametrize("page", ["page_single", "page_multisite"], indirect=True)
def test_management_catalog_copy(page: Page) -> None:
    """Test that each content type is available through the navigation."""

    expect(page.get_by_role("heading", name="Management")).to_be_visible()
    expect(page.locator("strong").filter(has_text="Catalogs")).to_be_visible()

    # open the copy form: click on the "Copy catalog" button
    # page.goto(f"/management/catalogs/1/copy")  # goto does not work with auto return after copy
    # page.locator('a[title="Copy catalog"]').first.click()
    page.get_by_title("Copy catalog").first.click()

    # expect the form is there with a URI Prefix field
    expect(page.get_by_role("textbox", name="URI Prefix")).to_be_visible()

    # create a copy of the catalog
    page.get_by_role("textbox", name="URI Path").click()
    page.get_by_role("textbox", name="URI Path").fill("catalog-copy")
    page.get_by_role("textbox", name="Title (English)").click()
    page.get_by_role("textbox", name="Title (English)").fill("Catalog copy")
    page.get_by_role("button", name="Copy").nth(1).click()
    # page.get_by_role("button", name="Copy").nth(1).click()

    # assert copy was successful
    # page.wait_for_url("/management/catalogs/")
    expect(page.locator("strong").filter(has_text="Catalogs")).to_be_visible()
    expect(page.get_by_role("link", name="http://example.com/terms/questions/catalog-copy")).to_be_visible()

    assert Catalog.objects.filter(uri="http://example.com/terms/questions/catalog-copy").exists()

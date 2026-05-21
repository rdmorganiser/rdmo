import pytest

from playwright.sync_api import Page, expect

from rdmo.questions.models import Catalog

pytestmark = pytest.mark.e2e


@pytest.mark.parametrize("page", ["page_single", "page_multisite"], indirect=True)
def test_management_catalog_copy(page: Page) -> None:
    """Test that each content type is available through the navigation."""
    source_uri = "http://example.com/terms/questions/catalog"
    copied_uri = "http://example.com/terms/questions/catalog-copy"
    copied_prefix = "http://example.com/terms"

    expect(page.get_by_role("heading", name="Management")).to_be_visible()
    expect(page.locator("strong").filter(has_text="Catalogs")).to_be_visible()

    # Open the copy form from the example.com catalog row.
    source_row = page.locator(".list-group-item").filter(
        has=page.get_by_role("link", name=source_uri, exact=True)
    )
    expect(source_row).to_be_visible()
    source_row.get_by_title("Copy catalog").click()

    # expect the form is there with a URI Prefix field
    expect(page.get_by_role("textbox", name="URI Prefix")).to_be_visible()

    # create a copy of the catalog
    page.get_by_role("textbox", name="URI Prefix").fill(copied_prefix)
    page.get_by_role("textbox", name="URI Path").click()
    page.get_by_role("textbox", name="URI Path").fill("catalog-copy")
    page.get_by_role("textbox", name="Title (English)").click()
    page.get_by_role("textbox", name="Title (English)").fill("Catalog copy")
    page.get_by_role("button", name="Copy").nth(1).click()
    # page.get_by_role("button", name="Copy").nth(1).click()

    # assert copy was successful
    # page.wait_for_url("/management/catalogs/")
    expect(page.locator("strong").filter(has_text="Catalogs")).to_be_visible()
    expect(page.get_by_role("link", name=copied_uri)).to_be_visible()

    assert Catalog.objects.filter(uri=copied_uri).exists()

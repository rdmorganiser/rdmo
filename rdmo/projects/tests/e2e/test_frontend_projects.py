import re

import pytest

from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e


def test_projects_page(page: Page):
    # Assert current page is correct
    expect(page).to_have_url(re.compile(r"/projects/$"))

    # Assert projects title and search bar
    expect(page.get_by_role("heading", name="All projects")).to_be_visible()
    expect(page.get_by_role("button", name="Import project")).to_be_visible()
    expect(page.get_by_role("button", name="New project")).to_be_visible()
    expect(page.get_by_role("textbox", name="Search projects")).to_be_visible()

    # Assert projects table
    expect(page.locator("thead")).to_contain_text("Name")
    expect(page.locator("tbody")).to_contain_text("Test")

    # Assert bottom of page
    page.locator("body").press("End")
    expect(page.get_by_role("button", name="Scroll to top")).to_be_visible()
    page.locator("body").press("Home")

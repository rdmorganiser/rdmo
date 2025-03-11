import re

import pytest

from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e


def test_project_detail_page(page: Page):
    # Assert current page is correct
    expect(page).to_have_url(re.compile(r"/projects/$"))

    # Arrange, click to go to Test project
    expect(page.get_by_role("link", name="Test", exact=True)).to_be_visible()
    page.get_by_role("link", name="Test", exact=True).click()
    expect(page).to_have_url(re.compile(r"/projects/1/?$"))

    # Assert project detail page
    expect(page.get_by_role("heading", name="Test")).to_be_visible()
    expect(page.get_by_role("link", name="Answer questions")).to_be_visible()

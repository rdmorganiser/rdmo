
from playwright.sync_api import Page, expect


def assert_warning_items(page: Page, expected_warnings) -> None:
    """Assert warning items inside the first .panel-import-warnings panel.

    Args:
        page: The current Playwright page instance.
        expected_warnings: A list of (label_text, code_uri, warning_text) tuples.
    """
    # Click to reveal the correct warning panel
    heading = f"Warnings ({len(expected_warnings)}):"
    page.get_by_text(heading).click()

    # Locate the first warning panel and its items
    warnings = page.locator(".panel-import-warnings").first.locator("ul.list-group > li.list-group-item")
    expect(warnings).to_have_count(len(expected_warnings))

    for i, (label_text, code_uri, warning_text) in enumerate(expected_warnings):
        item = warnings.nth(i)
        expect(item.locator("strong")).to_have_text(label_text)
        expect(item.locator("code")).to_have_text(code_uri)
        expect(item.locator(".text-warning")).to_have_text(warning_text)

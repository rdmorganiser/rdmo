# ruff: noqa: F811
import os
import re
from urllib.parse import urlparse

import pytest

from playwright.sync_api import Page, expect

from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute
from rdmo.questions.models import Catalog

from .helpers_models import ModelHelper, model_helpers

pytestmark = pytest.mark.e2e

# needed for playwright to run
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

test_users = [('editor', 'editor')]

@pytest.mark.parametrize("username,password", test_users)
@pytest.mark.parametrize("helper", model_helpers)
def test_management_navigation(logged_in_user: Page, helper: ModelHelper, username: str, password: str) -> None:
    """Test that each content type is available through the navigation."""
    page = logged_in_user
    expect(page.get_by_role("heading", name="Management")).to_be_visible()

    # click a link in the navigation
    name = helper.verbose_name_plural
    page.get_by_role("link", name=name, exact=True).click()

    # make sure the browser opened a new page
    url_name = name.lower()
    url_name = url_name.replace(" ", "")
    expect(page).to_have_url(re.compile(rf".*/{url_name}/"))

    # take a screenshot for visual inspection
    if helper.model == Catalog:
        item_in_ui = page.locator(".list-group > .list-group-item").first
        expect(item_in_ui).to_be_visible()
        page.screenshot(path="screenshots/management-navigation-catalog.png", full_page=True)



@pytest.mark.parametrize("username,password", test_users)
@pytest.mark.parametrize("helper", model_helpers)
def test_management_has_items(logged_in_user: Page, helper: ModelHelper) -> None:
    """Test all items in database are visible in management UI."""
    page = logged_in_user
    num_items_in_database = helper.model.objects.count()
    page.goto(f"/management/{helper.url}")
    items_in_ui = page.locator(".list-group > .list-group-item")
    expect(items_in_ui).to_have_count(num_items_in_database)


@pytest.mark.parametrize("username,password", test_users)
@pytest.mark.parametrize("helper", model_helpers)
def test_management_nested_view(
    logged_in_user: Page, helper: ModelHelper
) -> None:
    """For each element type, that has a nested view, click the first example."""
    page = logged_in_user
    page.goto(f"/management/{helper.url}")
    # Open nested view for element type
    if helper.has_nested:
        page.get_by_title(f"View {helper.verbose_name} nested").first.click()
        expect(page.locator(".panel-default").first).to_be_visible()
        expect(page.locator(".panel-default > .panel-body").first).to_be_visible()


@pytest.mark.parametrize("username,password", test_users)
@pytest.mark.parametrize("helper", model_helpers)
def test_management_create_model(
    logged_in_user: Page, helper: ModelHelper
) -> None:
    """Test management UI can create objects in the database."""
    page = logged_in_user
    num_objects_at_start = helper.model.objects.count()
    page.goto(f"/management/{helper.url}")
    # click "New" button
    page.get_by_role("button", name="New").click()
    # fill mandatory fields
    value = "some-value"
    page.get_by_label(helper.form_field).fill(value)
    if helper.model == Condition:
        # conditions need to have a source attribute
        source_form = (
            page.locator(".form-group")
            .filter(has_text="Source")
            .locator(".select-item > .react-select")
        )
        source_form.click()
        page.keyboard.type(Attribute.objects.first().uri)
        page.keyboard.press("Enter")

    # save
    page.get_by_role("button", name="Create").nth(1).click()
    # check if new item is in list
    items_in_ui = page.locator(".list-group > .list-group-item")
    expect(items_in_ui).to_have_count(num_objects_at_start + 1)

    num_objects_after_save = helper.model.objects.count()
    assert num_objects_after_save - num_objects_at_start == 1
    query = {helper.db_field: value}
    assert helper.model.objects.get(**query)


@pytest.mark.parametrize("username,password", test_users)
@pytest.mark.parametrize("helper", model_helpers)
def test_management_edit_model(logged_in_user: Page, helper: ModelHelper) -> None:
    page = logged_in_user
    page.goto(f"/management/{helper.url}")
    # click edit
    edit_button_title = f"Edit {helper.verbose_name}"
    page.get_by_title(f"{edit_button_title}").first.click()
    # edit
    page.get_by_label("Comment").click()
    comment = "this is a comment."
    page.get_by_label("Comment").fill(comment)
    # save
    page.get_by_role("button", name="Save").nth(1).click()
    # click on edit element again
    page.get_by_title(f"{edit_button_title}").first.click()
    # check the updated comment
    comment_locator = page.get_by_label("Comment")
    expect(comment_locator).to_have_text(comment)
    # compare the updated comment with element object from db
    url_id = int(urlparse(page.url).path.rstrip("/").split("/")[-1])
    model_obj = helper.model.objects.get(id=url_id)
    assert model_obj.comment == comment

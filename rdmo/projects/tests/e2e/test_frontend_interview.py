import re

import pytest

from playwright.sync_api import Page, Response, expect

from rdmo.projects.models import Value
from rdmo.questions.models import Question

pytestmark = [pytest.mark.e2e, pytest.mark.django_db(transaction=True)]


def test_add_collection_value_preserves_default_external_id(page: Page):
    question = Question.objects.get(pk=93)
    question.is_collection = True
    question.save(update_fields=("is_collection",))

    value_filter = {
        "project_id": 1,
        "attribute_id": question.attribute_id,
        "snapshot": None,
    }
    Value.objects.filter(**value_filter).delete()

    def is_values_refresh(response: Response) -> bool:
        return (
            response.request.method == "GET" and
            re.search(r"/api/v1/projects/projects/1/values/\?", response.url) is not None
        )

    # Progress updates are unrelated and otherwise race value requests when the e2e suite uses SQLite.
    page.route(
        "**/api/v1/projects/projects/1/progress/",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"count": 0, "total": 0, "ratio": 0}',
        ),
    )

    page.goto("/projects/1/interview/85/")

    widgets = page.locator(".interview-question .interview-widget")
    expect(widgets).to_have_count(1)
    expect(widgets.nth(0)).to_contain_text("Simple answer 1")
    expect(widgets.nth(0).get_by_text("Default", exact=True)).to_be_visible()

    with page.expect_response(is_values_refresh):
        page.get_by_role("button", name="Add answer").click()

    expect(widgets).to_have_count(2)
    expect(widgets.nth(0)).to_contain_text("Simple answer 1")
    expect(widgets.nth(1).locator(".react-select__placeholder")).to_have_text("Select ...")

    widgets.nth(1).get_by_role("combobox").click()
    option = page.get_by_role("option").filter(has_text="Simple answer 2")
    with page.expect_response(is_values_refresh):
        option.click()

    expect(widgets).to_have_count(2)
    expect(widgets.nth(0)).to_contain_text("Simple answer 1")
    expect(widgets.nth(1)).to_contain_text("Simple answer 2")

    page.reload()

    expect(widgets).to_have_count(2)
    expect(widgets.nth(0)).to_contain_text("Simple answer 1")
    expect(widgets.nth(1)).to_contain_text("Simple answer 2")

    values = Value.objects.filter(**value_filter).order_by("collection_index")
    assert list(values.values_list("collection_index", "external_id")) == [
        (0, "simple_1"),
        (1, "simple_2"),
    ]

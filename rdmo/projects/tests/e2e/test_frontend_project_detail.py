import re

import pytest

from playwright.sync_api import Page, expect

from rdmo.projects.models import Project

pytestmark = [pytest.mark.e2e, pytest.mark.django_db(transaction=True)]


def test_project_detail_page(page: Page):
    project = Project.objects.get(id=1)

    # Assert current page is correct
    expect(page).to_have_url(re.compile(r'/projects/$'))

    # Arrange, click to go to Test project
    expect(page.get_by_role('link', name='Test', exact=True)).to_be_visible()
    page.get_by_role('link', name='Test', exact=True).click()
    expect(page).to_have_url(re.compile(r'/projects/1/?$'))
    page.screenshot(path='screenshots/projects/project-detail.png', full_page=True)

    # Assert project detail page
    expect(page.get_by_role('heading', name='Test')).to_be_visible()

    for issue in project.issues.all():
        if issue.resolve:
            if issue.task.task_type in ['step', 'guidance']:
                expect(page.get_by_role('heading', name=issue.task.title)).to_be_visible()
            else:
                expect(page.get_by_text(issue.task.title)).to_be_visible()

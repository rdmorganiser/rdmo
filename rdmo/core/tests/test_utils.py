from http import HTTPStatus
from typing import Optional

import pytest

from rdmo.core.utils import human2bytes, join_url, render_to_format, sanitize_url
from rdmo.projects.models import Project
from rdmo.projects.utils import get_value_path
from rdmo.views.utils import ProjectWrapper

urls = (
    ('', ''),
    ('/', ''),
    ('foo', 'foo'),
    ('/foo', '/foo'),
    ('/foo/', '/foo/'),
    ('foo/bar', 'foo/bar'),
    ('foo/bar/', 'foo/bar/'),
    ('/foo/bar', '/foo/bar'),
    ('/foo/bar/', '/foo/bar/'),
    (1, ''),
)

human2bytes_test_values = (
    ("1Gb", 1e+9),
    (None, 0),
    ("0", 0),
)

export_formats = ("invalid", "rtf", "odt", "docx", "html", "markdown", "tex", "pdf")


@pytest.mark.parametrize('url,sanitized_url', urls)
def test_sanitize_url(url, sanitized_url):
    assert sanitize_url(url) == sanitized_url


def test_join_url():
    assert join_url('https://example.com//', '/terms', 'foo') == 'https://example.com/terms/foo'


@pytest.mark.parametrize('human,bytes', human2bytes_test_values)
def test_human2bytes(human: Optional[str], bytes: float):
    assert human2bytes(human) == bytes


@pytest.fixture(scope="module")
def context(django_db_blocker):
    """A fixture of a view context, to be used when testing 'render_to_format'.

    Note: The fixture queries the database only once for the parametrized tests.
    """
    with django_db_blocker.unblock():
        project = Project.objects.get(id=1)
        project.catalog.prefetch_elements()
        return {
            "format": None, # will be defined in the test function
            "project": project,
            "project_wrapper": ProjectWrapper(project),
            "title": project.title,
            "resource_path": get_value_path(project)
        }


@pytest.mark.django_db()
@pytest.mark.parametrize("export_format", export_formats)
def test_render_to_format(rf, context, export_format):
    """A test of the 'render_to_format' view with multiple export formats."""
    context["format"] = export_format
    title = context["project"].title

    request = rf.get("/projects/project_answers_export")
    response = render_to_format(
        request,
        export_format,
        title,
        "projects/project_answers_export.html",
        context,
    )

    # an invalid export format should return an error message
    if export_format == "invalid":
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "This format is not supported." in str(response.content)
        return
    # check for the requested export format in the headers
    assert response.status_code == HTTPStatus.OK
    assert export_format in response.headers["Content-Type"]
    expected = f'filename="{title}.{export_format}"'
    assert expected in response.headers["Content-Disposition"]

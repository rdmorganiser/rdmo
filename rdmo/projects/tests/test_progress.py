import pytest

from rdmo.projects.models import Project
from rdmo.projects.progress import compute_page, compute_progress
from rdmo.questions.models import Page

projects = [1, 11]

results_map = {
    1: (84, 136),
    11: (0, 62)
}


@pytest.mark.parametrize('project_id', projects)
def test_compute_progress(db, project_id):
    project = Project.objects.get(id=project_id)
    project.catalog.prefetch_elements()

    progress = compute_progress(project)

    assert progress == results_map[project_id]


def test_compute_progress_without_catalog(db):
    project = Project.objects.get(pk=1)
    project.catalog = None

    assert compute_progress(project) == (0, 0)


@pytest.mark.parametrize('direction', ['next', 'prev'])
def test_compute_page_without_catalog(db, direction):
    project = Project.objects.get(pk=1)
    project.catalog = None

    assert compute_page(project, Page(pk=1), direction) is None

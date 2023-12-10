import pytest

from rdmo.projects.models import Project
from rdmo.projects.progress import compute_progress

projects = [1, 11]

results_map = {
    1: (55, 84),
    11: (0, 29)
}


@pytest.mark.parametrize('project_id', projects)
def test_compute_progress(db, project_id):
    project = Project.objects.get(id=project_id)
    project.catalog.prefetch_elements()

    progress = compute_progress(project)

    assert progress == results_map[project_id]

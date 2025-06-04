
from rdmo.projects.models import Project
from rdmo.projects.tests.helpers.project_sync.catalog_views import get_catalog_task_mapping, get_catalog_view_mapping
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
from rdmo.views.models import View

project_id = 10


def test_project_views_sync_when_changing_the_catalog_on_a_project(
        db, settings, enable_project_views_sync
):
    assert settings.PROJECT_VIEWS_SYNC

    # Setup: Create a catalog, a view, and a project using the catalog
    project = Project.objects.get(id=project_id)
    initial_project_views = set(project.views.values_list('id', flat=True))
    assert initial_project_views == {1,2,3}  # from the fixture

    catalog_view_mapping = get_catalog_view_mapping()
    for catalog_id, view_ids in catalog_view_mapping.items():
        if project.catalog_id == catalog_id:
            continue  # catalog will not change
        project.catalog = Catalog.objects.get(id=catalog_id)
        project.save()

        # TODO this filter_available_views_for_project method needs to tested explicitly
        available_views = set(
            View.objects
                .filter_for_project(project)
                .filter_availability(project.owners.first())
                .values_list('id', flat=True)
        )
        assert set(project.views.values_list('id', flat=True)) == available_views



def test_project_tasks_sync_when_changing_the_catalog_on_a_project(
        db, settings, enable_project_tasks_sync
):
    assert settings.PROJECT_TASKS_SYNC

    # Setup: Create a catalog, a task, and a project using the catalog
    project = Project.objects.get(id=project_id)
    initial_project_tasks = set(project.tasks.values_list('id', flat=True))
    assert initial_project_tasks == {1,2}  # from the fixture

    catalog_task_mapping = get_catalog_task_mapping()
    for catalog_id, task_ids in catalog_task_mapping.items():
        if project.catalog_id == catalog_id:
            continue  # catalog will not change
        project.catalog = Catalog.objects.get(id=catalog_id)
        project.save()

        # TODO this filter_available_tasks_for_project method needs to tested explicitly
        available_tasks = set(
            Task.objects
                .filter_for_project(project)
                .filter_availability(project.owners.first())
                .values_list('id', flat=True)
        )
        assert set(project.tasks.values_list('id', flat=True)) == available_tasks

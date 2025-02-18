
from django.contrib.auth.models import Group

from rdmo.projects.models import Project
from rdmo.tasks.models import Task

from .helpers import (
    assert_other_projects_unchanged,
    enable_project_tasks_sync,  # noqa: F401
)

project_id = 10
task_id = 1
group_name = 'view_test'

def test_project_tasks_sync_when_adding_or_removing_a_catalog_to_or_from_a_task(
        db, settings, enable_project_tasks_sync  # noqa:F811
    ):
    assert settings.PROJECT_TASKS_SYNC

    # Setup: Create a catalog, a task, and a project using the catalog
    project = Project.objects.get(id=project_id)
    catalog = project.catalog
    other_projects = Project.objects.exclude(catalog=catalog)  # All other projects
    task = Task.objects.get(id=task_id)  # This task does not have catalogs in the fixture
    task.catalogs.clear()
    initial_project_tasks = project.tasks.values_list('id', flat=True)

    # Save initial state of tasks for other projects
    initial_other_project_tasks = {
        i.id: list(i.tasks.values_list('id', flat=True))
        for i in other_projects
    }

    # Ensure the project does not have the task initially
    assert task not in project.tasks.all()

    ## Tests for .add and .remove
    # Add the catalog to the task and assert that the project now includes the task
    task.catalogs.add(catalog)
    assert task in project.tasks.all()
    assert_other_projects_unchanged(other_projects, initial_other_project_tasks)

    # Remove the catalog from the task and assert that the project no longer includes the task
    task.catalogs.remove(catalog)
    assert task not in project.tasks.all()
    assert_other_projects_unchanged(other_projects, initial_other_project_tasks)

    ## Tests for .set and .clear
    # Add the catalog to the task and assert that the project now includes the task
    task.catalogs.set([catalog])
    assert task in project.tasks.all()
    assert_other_projects_unchanged(other_projects, initial_other_project_tasks)

    # Remove all catalogs from the task and assert that the project no longer includes the task
    task.catalogs.clear()
    assert task not in project.tasks.all()
    assert_other_projects_unchanged(other_projects, initial_other_project_tasks)

    # Assert that the initial project tasks are unchanged
    assert set(project.tasks.values_list('id', flat=True)) == set(initial_project_tasks)


def test_project_tasks_sync_when_adding_or_removing_a_site_to_or_from_a_task(
        db, settings, enable_project_tasks_sync  # noqa:F811
    ):
    assert settings.PROJECT_TASKS_SYNC

    # Setup: Get an existing project, its associated site, and create a task
    project = Project.objects.get(id=project_id)
    site = project.site
    other_projects = Project.objects.exclude(site=site)  # All other projects
    task = Task.objects.get(id=task_id)  # This task does not have sites in the fixture
    task.sites.clear()  # Ensure the task starts without any sites
    project.tasks.remove(task)
    initial_project_tasks = project.tasks.values_list('id', flat=True)

    # Save initial state of tasks for other projects
    initial_other_project_tasks = {
        i.id: list(i.tasks.values_list('id', flat=True))
        for i in other_projects
    }

    # Ensure the project does not have the task initially
    assert task not in project.tasks.all()

    ## Tests for .add and .remove
    # Add the site to the task and assert that the project now includes the task
    task.sites.add(site)
    assert task in project.tasks.all()
    assert_other_projects_unchanged(other_projects, initial_other_project_tasks)

    # Remove the site from the task and assert that the project no longer includes the task
    task.sites.remove(site)
    assert task not in project.tasks.all()
    assert_other_projects_unchanged(other_projects, initial_other_project_tasks)

    ## Tests for .set and .clear
    # Add the site to the task and assert that the project now includes the task
    task.sites.set([site])
    assert task in project.tasks.all()
    assert_other_projects_unchanged(other_projects, initial_other_project_tasks)

    # Clear all sites from the task and assert that the project no longer includes the task
    task.sites.clear()
    assert task not in project.tasks.all()
    assert_other_projects_unchanged(other_projects, initial_other_project_tasks)

    # Assert that the initial project tasks are unchanged
    assert set(project.tasks.values_list('id', flat=True)) == set(initial_project_tasks)


def test_project_tasks_sync_when_adding_or_removing_a_group_to_or_from_a_task(
        db, settings, enable_project_tasks_sync  # noqa:F811
    ):
    assert settings.PROJECT_TASKS_SYNC

    # Setup: Get an existing project, its associated group, and create a task
    project = Project.objects.get(id=project_id)
    user = project.owners.first()  # Get the first user associated with the project
    group = Group.objects.filter(name=group_name).first()  # Get a test group
    user.groups.add(group)
    other_projects = Project.objects.exclude(memberships__user=user)  # All other projects
    task = Task.objects.get(id=task_id)  # This task does not have groups in the fixture
    task.groups.clear()  # Ensure the task starts without any groups
    initial_project_tasks = project.tasks.values_list('id', flat=True)

    # Save initial state of tasks for other projects
    initial_other_project_tasks = {
        i.id: list(i.tasks.values_list('id', flat=True))
        for i in other_projects
    }

    # Ensure the project does not have the task initially
    assert task not in project.tasks.all()

    ## Tests for .add and .remove
    # Add the group to the task and assert that the project now includes the task
    task.groups.add(group)
    assert task in project.tasks.all()
    assert_other_projects_unchanged(other_projects, initial_other_project_tasks)

    # Remove the group from the task and assert that the project no longer includes the task
    task.groups.remove(group)
    assert task not in project.tasks.all()
    assert_other_projects_unchanged(other_projects, initial_other_project_tasks)

    ## Tests for .set and .clear
    # Add the group to the task and assert that the project now includes the task
    task.groups.set([group])
    assert task in project.tasks.all()
    assert_other_projects_unchanged(other_projects, initial_other_project_tasks)

    # Clear all groups from the task and assert that the project no longer includes the task
    task.groups.clear()
    assert task not in project.tasks.all()
    assert_other_projects_unchanged(other_projects, initial_other_project_tasks)

    # Assert that the initial project tasks are unchanged
    assert set(project.tasks.values_list('id', flat=True)) == set(initial_project_tasks)

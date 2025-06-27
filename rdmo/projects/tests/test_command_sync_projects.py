import pytest

from django.core.management import call_command

from rdmo.projects.tests.helpers.project_sync.arrange_project_tasks import arrange_projects_catalogs_and_tasks
from rdmo.projects.tests.helpers.project_sync.arrange_project_views import arrange_projects_catalogs_and_views
from rdmo.projects.tests.helpers.project_sync.assert_cli_output import assert_sync_projects_show_has_output
from rdmo.projects.tests.helpers.project_sync.assert_project_views_or_tasks import (
    assert_all_projects_are_synced_with_instance_m2m_field,
)

PROJECT_SHOW_TEMPLATE = 'Project "{}" [id={}]:'

@pytest.mark.django_db
def test_command_sync_projects_for_tasks(settings, enable_project_tasks_sync):
    assert settings.PROJECT_TASKS_SYNC

    # Arrange: pre-linked projects and catalog-based task relationships
    P, C, T = arrange_projects_catalogs_and_tasks()

    # Arrange: project.tasks are in a random initial state
    P[1].tasks.set([T[1], T[2], T[3]])
    P[2].tasks.clear()
    P[3].tasks.set([T[2]])

    # === Act: run the management command for task sync ===
    call_command('sync_projects', '--tasks')

    # === Assert: each project should only be linked to tasks with matching catalogs ===
    assert set(P[1].tasks.all()) == {T[1]}
    assert set(P[2].tasks.all()) == {T[2]}
    assert set(P[3].tasks.all()) == {T[3]}

    # Additional assertion using your existing helper
    for task in T.values():
        assert_all_projects_are_synced_with_instance_m2m_field(task, 'catalogs')


@pytest.mark.django_db
def test_command_sync_projects_for_views(settings, enable_project_views_sync):
    assert settings.PROJECT_VIEWS_SYNC

    # Arrange: pre-linked projects and catalog-based view relationships
    P, C, V = arrange_projects_catalogs_and_views()

    # Arrange: project.views are in a random initial state
    P[1].views.set([V[1], V[2]])
    P[2].views.clear()
    P[3].views.set([V[1]])

    # === Act: run the management command for view sync ===
    call_command('sync_projects', '--views')

    # === Assert: each project should only be linked to views with matching catalogs ===
    assert set(P[1].views.all()) == {V[1]}
    assert set(P[2].views.all()) == {V[2]}
    assert set(P[3].views.all()) == {V[3]}

    for view in V.values():
        assert_all_projects_are_synced_with_instance_m2m_field(view, 'catalogs')


@pytest.mark.django_db
def test_command_sync_projects_show_and_tasks_displays_output(settings, enable_project_tasks_sync, capsys):

    call_command('sync_projects', '--tasks', '--show')

    out_lines = capsys.readouterr().out.splitlines()
    assert_sync_projects_show_has_output(out_lines)



@pytest.mark.django_db
def test_command_sync_projects_show_and_views_displays_output(settings, enable_project_views_sync, capsys):

    call_command('sync_projects', '--views', '--show')

    out_lines = capsys.readouterr().out.splitlines()
    assert_sync_projects_show_has_output(out_lines)



@pytest.mark.django_db
def test_command_sync_projects_for_tasks_and_views_with_show(
        settings,
        enable_project_tasks_sync, enable_project_views_sync,
        capsys
    ):
    assert settings.PROJECT_TASKS_SYNC
    assert settings.PROJECT_VIEWS_SYNC

    # Arrange task and view state
    P1, C1, T = arrange_projects_catalogs_and_tasks()
    P2, C2, V = arrange_projects_catalogs_and_views()

    # Arrange random desynced state
    P1[1].tasks.set([T[1], T[2], T[3]])
    P1[2].tasks.clear()
    P1[3].tasks.set([T[2]])

    P2[1].views.set([V[1], V[2]])
    P2[2].views.clear()
    P2[3].views.set([V[1]])

    # === Act: run sync with both flags and show output ===
    call_command('sync_projects', '--tasks', '--views', '--show')

    # === Assert: state is fully synced
    assert set(P1[1].tasks.all()) == {T[1]}
    assert set(P1[2].tasks.all()) == {T[2]}
    assert set(P1[3].tasks.all()) == {T[3]}

    assert set(P2[1].views.all()) == {V[1]}
    assert set(P2[2].views.all()) == {V[2]}
    assert set(P2[3].views.all()) == {V[3]}

    for task in T.values():
        assert_all_projects_are_synced_with_instance_m2m_field(task, 'catalogs')

    for view in V.values():
        assert_all_projects_are_synced_with_instance_m2m_field(view, 'catalogs')

    # === Assert: show output includes all project/task/view
    out_lines = capsys.readouterr().out.splitlines()
    assert_sync_projects_show_has_output(out_lines)

import pytest

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management import call_command

from rdmo.projects.models import Membership, Project
from rdmo.projects.tests.helpers.sync.arrange_project_tasks import arrange_projects_catalogs_and_tasks
from rdmo.projects.tests.helpers.sync.arrange_project_views import arrange_projects_catalogs_and_views
from rdmo.projects.tests.helpers.sync.assert_cli_output import assert_sync_projects_show_has_output
from rdmo.projects.tests.helpers.sync.assert_project_views_or_tasks import (
    assert_all_projects_are_synced_with_instance_m2m_field,
    assert_other_tasks_remain_synced,
    assert_other_views_remain_synced,
)
from rdmo.projects.tests.helpers.sync.project_relation_ids import project_relation_ids
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
from rdmo.views.models import View

PROJECT_SHOW_TEMPLATE = 'Project "{}" [id={}]:'


@pytest.mark.django_db
def test_command_sync_projects_for_tasks(settings):
    settings.PROJECT_TASKS_SYNC = True

    # Arrange: pre-linked projects and catalog-based task relationships
    P, _, T = arrange_projects_catalogs_and_tasks()
    task_ids = [task.pk for task in T.values()]

    # Arrange: project.tasks are in a random initial state
    P[1].tasks.set([T[1], T[2], T[3]])
    P[2].tasks.clear()
    P[3].tasks.set([T[2]])

    # === Act: run the management command for task sync ===
    call_command('sync_projects', '--tasks')

    # === Assert: each project should only be linked to tasks with matching catalogs and sites ===
    assert set(P[1].tasks.filter(pk__in=task_ids)) == {T[1]}
    assert set(P[2].tasks.filter(pk__in=task_ids)) == {T[2]}
    assert set(P[3].tasks.filter(pk__in=task_ids)) == {T[3]}

    for project in Project.objects.all():
        assert_other_tasks_remain_synced(project, task_ids)

    # Additional assertion using your existing helper
    for task in T.values():
        assert_all_projects_are_synced_with_instance_m2m_field(task, 'catalogs')


@pytest.mark.django_db
def test_command_sync_projects_for_views(settings):
    settings.PROJECT_VIEWS_SYNC = True

    # Arrange: pre-linked projects and catalog-based view relationships
    P, _, V = arrange_projects_catalogs_and_views()
    view_ids = [view.pk for view in V.values()]

    # Arrange: project.views are in a random initial state
    P[1].views.set([V[1], V[2]])
    P[2].views.clear()
    P[3].views.set([V[1]])

    # === Act: run the management command for view sync ===
    call_command('sync_projects', '--views')

    # === Assert: each project should only be linked to views with matching catalogs ===
    assert set(P[1].views.filter(pk__in=view_ids)) == {V[1]}
    assert set(P[2].views.filter(pk__in=view_ids)) == {V[2]}
    assert set(P[3].views.filter(pk__in=view_ids)) == {V[3]}

    for project in Project.objects.all():
        assert_other_views_remain_synced(project, view_ids)

    for view in V.values():
        assert_all_projects_are_synced_with_instance_m2m_field(view, 'catalogs')


@pytest.mark.django_db
def test_command_sync_projects_show_and_tasks_displays_output(settings, capsys):
    settings.PROJECT_TASKS_SYNC = True

    call_command('sync_projects', '--tasks', '--show')

    out_lines = capsys.readouterr().out.splitlines()
    assert_sync_projects_show_has_output(out_lines)


@pytest.mark.django_db
def test_command_sync_projects_show_and_views_displays_output(settings, capsys):
    settings.PROJECT_VIEWS_SYNC = True

    call_command('sync_projects', '--views', '--show')

    out_lines = capsys.readouterr().out.splitlines()
    assert_sync_projects_show_has_output(out_lines)


@pytest.mark.django_db
def test_command_sync_projects_for_tasks_and_views_with_show(settings, capsys):
    settings.PROJECT_TASKS_SYNC = True
    settings.PROJECT_VIEWS_SYNC = True

    # Arrange task and view state
    P1, _, T = arrange_projects_catalogs_and_tasks()
    P2, _, V = arrange_projects_catalogs_and_views()
    task_ids = [task.pk for task in T.values()]
    view_ids = [view.pk for view in V.values()]

    # Arrange random desynced state
    P1[1].tasks.set([T[1], T[2], T[3]])
    P1[2].tasks.clear()
    P1[3].tasks.set([T[2]])

    P2[1].views.set([V[1], V[2]])
    P2[2].views.clear()
    P2[3].views.set([V[1]])

    # === Act: run sync with both flags and show output ===
    call_command('sync_projects', '--tasks', '--views', '--show')

    # Assert catalog reconciliation among the controlled tasks and views.
    assert set(P1[1].tasks.filter(pk__in=task_ids)) == {T[1]}
    assert set(P1[2].tasks.filter(pk__in=task_ids)) == {T[2]}
    assert set(P1[3].tasks.filter(pk__in=task_ids)) == {T[3]}

    assert set(P2[1].views.filter(pk__in=view_ids)) == {V[1]}
    assert set(P2[2].views.filter(pk__in=view_ids)) == {V[2]}
    assert set(P2[3].views.filter(pk__in=view_ids)) == {V[3]}

    for project in Project.objects.all():
        assert_other_tasks_remain_synced(project, task_ids)
        assert_other_views_remain_synced(project, view_ids)

    for task in T.values():
        assert_all_projects_are_synced_with_instance_m2m_field(task, 'catalogs')

    for view in V.values():
        assert_all_projects_are_synced_with_instance_m2m_field(view, 'catalogs')

    # === Assert: show output includes all project/task/view
    out_lines = capsys.readouterr().out.splitlines()
    assert_sync_projects_show_has_output(out_lines)


@pytest.mark.django_db
@pytest.mark.parametrize('model,field', [(Task, 'tasks'), (View, 'views')])
def test_command_sync_projects_unrestricted_instance(settings, model, field):
    settings.PROJECT_TASKS_SYNC = False
    settings.PROJECT_VIEWS_SYNC = False
    settings.MULTISITE = False

    site = Site.objects.get(pk=1)
    instance = model.objects.create(uri_prefix='http://example.com/test', uri_path='sync-unrestricted')
    instance.sites.add(site)
    other_project = Project.objects.create(
        title='Sync other site', catalog=Catalog.objects.get(pk=1), site=Site.objects.get(pk=2)
    )
    # Set a wrong-site relation and leave matching projects missing the instance.
    instance.projects.set([other_project])
    expected_projects = set(Project.objects.filter(site=site))

    setattr(settings, f'PROJECT_{field.upper()}_SYNC', True)
    call_command('sync_projects', f'--{field}')

    assert set(instance.projects.all()) == expected_projects
    first_state = project_relation_ids(field)
    call_command('sync_projects', f'--{field}')
    assert project_relation_ids(field) == first_state


@pytest.mark.django_db
@pytest.mark.parametrize('model,field', [(Task, 'tasks'), (View, 'views')])
def test_command_sync_projects_unavailable_instance(settings, capsys, model, field):
    settings.PROJECT_TASKS_SYNC = False
    settings.PROJECT_VIEWS_SYNC = False
    settings.MULTISITE = False

    catalog, site = Catalog.objects.get(pk=1), Site.objects.get(pk=1)
    normal_project = Project.objects.create(title='Sync normal member', catalog=catalog, site=site)
    privileged_project = Project.objects.create(title='Sync privileged member', catalog=catalog, site=site)
    empty_project = Project.objects.create(title='Sync no members', catalog=catalog, site=site)
    normal_user = User.objects.create(username='sync-normal')
    privileged_user = User.objects.create(username='sync-privileged', is_superuser=True)
    Membership.objects.create(project=normal_project, user=normal_user, role='owner')
    Membership.objects.create(project=privileged_project, user=privileged_user, role='owner')

    instance = model.objects.create(
        uri_prefix='http://example.com/test', uri_path='sync-unavailable', available=False
    )
    instance.catalogs.add(catalog)
    instance.sites.add(site)
    instance.projects.set([normal_project, empty_project])

    setattr(settings, f'PROJECT_{field.upper()}_SYNC', True)
    call_command('sync_projects', f'--{field}')

    # Independent expectations also cover the command's no-member behavior.
    assert instance not in getattr(normal_project, field).all()
    assert instance not in getattr(empty_project, field).all()
    assert instance in getattr(privileged_project, field).all()
    assert (
        f'Starting sync for {model.objects.count()} {model._meta.verbose_name_plural}...'
        in capsys.readouterr().out
    )

    first_state = project_relation_ids(field)
    call_command('sync_projects', f'--{field}')
    assert project_relation_ids(field) == first_state

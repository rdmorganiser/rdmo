import pytest

from rdmo.projects.tests.helpers.sync.arrange_project_tasks import arrange_projects_catalogs_and_tasks
from rdmo.projects.tests.helpers.sync.arrange_project_views import arrange_projects_catalogs_and_views
from rdmo.projects.tests.helpers.sync.assert_project_views_or_tasks import (
    assert_other_tasks_remain_synced,
    assert_other_views_remain_synced,
)


@pytest.mark.django_db
def test_project_tasks_sync_when_changing_a_catalog_on_a_project(settings):
    settings.PROJECT_TASKS_SYNC = True

    P, C, T = arrange_projects_catalogs_and_tasks()
    task_ids = [task.pk for task in T.values()]
    initial_p3_tasks = set(P[3].tasks.all())
    # === Initial state ===
    # P1 (with C1) has T1 among the controlled tasks, etc.
    assert set(P[1].tasks.filter(pk__in=task_ids)) == {T[1]}
    assert set(P[2].tasks.filter(pk__in=task_ids)) == {T[2]}
    assert set(P[3].tasks.filter(pk__in=task_ids)) == {T[3]}
    # Act: change catalog on P1 and P2
    P[1].catalog = C[2]
    P[1].save()
    P[2].catalog = C[1]
    P[2].save()
    # Assert: T1 and T2 were swapped
    assert set(P[1].tasks.filter(pk__in=task_ids)) == {T[2]}
    assert set(P[2].tasks.filter(pk__in=task_ids)) == {T[1]}
    assert set(P[3].tasks.filter(pk__in=task_ids)) == {T[3]}

    for project in (P[1], P[2]):
        assert_other_tasks_remain_synced(project, task_ids)
    # P3 was not resynchronized; preserve its complete arranged relation.
    assert set(P[3].tasks.all()) == initial_p3_tasks


@pytest.mark.django_db
def test_project_views_sync_when_changing_a_catalog_on_a_project(settings):
    settings.PROJECT_VIEWS_SYNC = True

    P, C, V = arrange_projects_catalogs_and_views()
    view_ids = [view.pk for view in V.values()]
    initial_p3_views = set(P[3].views.all())
    # === Initial state ===
    # P1 (with C1) has V1, etc..
    assert set(P[1].views.filter(pk__in=view_ids)) == {V[1]}
    assert set(P[2].views.filter(pk__in=view_ids)) == {V[2]}
    assert set(P[3].views.filter(pk__in=view_ids)) == {V[3]}
    # Act: change catalog on P1 and P2
    P[1].catalog = C[2]
    P[1].save()
    P[2].catalog = C[1]
    P[2].save()
    # Assert: V1 and V2 were swapped
    assert set(P[1].views.filter(pk__in=view_ids)) == {V[2]}
    assert set(P[2].views.filter(pk__in=view_ids)) == {V[1]}
    assert set(P[3].views.filter(pk__in=view_ids)) == {V[3]}

    for project in (P[1], P[2]):
        assert_other_views_remain_synced(project, view_ids)
    assert set(P[3].views.all()) == initial_p3_views

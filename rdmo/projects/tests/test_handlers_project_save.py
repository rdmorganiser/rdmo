import pytest

from rdmo.projects.tests.helpers.project_sync.arrange_project_tasks import arrange_projects_catalogs_and_tasks
from rdmo.projects.tests.helpers.project_sync.arrange_project_views import arrange_projects_catalogs_and_views


@pytest.mark.django_db
def test_project_tasks_sync_when_changing_a_catalog_on_a_project(settings, enable_project_tasks_sync):
    assert settings.PROJECT_TASKS_SYNC

    P, C, T = arrange_projects_catalogs_and_tasks()
    # === Initial state ===
    # P1 (with C1) has V1, etc..
    assert set(P[1].tasks.all()) == {T[1]}
    assert set(P[2].tasks.all()) == {T[2]}
    assert set(P[3].tasks.all()) == {T[3]}
    # Act: change catalog on P1 and P2
    P[1].catalog = C[2]
    P[1].save()
    P[2].catalog = C[1]
    P[2].save()
    # Assert: T1 and T2 were swapped
    assert set(P[1].tasks.all()) == {T[2]}
    assert set(P[2].tasks.all()) == {T[1]}
    assert set(P[3].tasks.all()) == {T[3]}


@pytest.mark.django_db
def test_project_views_sync_when_changing_a_catalog_on_a_project(settings, enable_project_views_sync):
    assert settings.PROJECT_VIEWS_SYNC

    P, C, V = arrange_projects_catalogs_and_views()
    # === Initial state ===
    # P1 (with C1) has V1, etc..
    assert set(P[1].views.all()) == {V[1]}
    assert set(P[2].views.all()) == {V[2]}
    assert set(P[3].views.all()) == {V[3]}
    # Act: change catalog on P1 and P2
    P[1].catalog = C[2]
    P[1].save()
    P[2].catalog = C[1]
    P[2].save()
    # Assert: T1 and T2 were swapped
    assert set(P[1].views.all()) == {V[2]}
    assert set(P[2].views.all()) == {V[1]}
    assert set(P[3].views.all()) == {V[3]}

import pytest

from rdmo.projects.models import Project
from rdmo.projects.tests.helpers.project_sync.arrange_project_tasks import arrange_projects_catalogs_and_tasks
from rdmo.projects.tests.helpers.project_sync.assert_project_views_or_tasks import (
    assert_all_projects_are_synced_with_instance_m2m_field,
)

P_TITLE = "Sync P{}"
one_two_three = (1, 2, 3)

@pytest.mark.django_db
def test_project_tasks_sync_when_updating_task_catalogs(settings, enable_project_tasks_sync):
    assert settings.PROJECT_TASKS_SYNC

    P, C, T = arrange_projects_catalogs_and_tasks()

    # === Initial state ===
    # P1 (with C1) has T1, etc..
    assert set(P[1].tasks.all()) == {T[1]}
    assert set(P[2].tasks.all()) == {T[2]}
    assert set(P[3].tasks.all()) == {T[3]}

    # === Update: T1 has no catalogs → it should appear in all projects ===
    T[1].catalogs.clear()
    assert set(P[1].tasks.all()) == {T[1]}  # should remain unchanged
    assert set(P[2].tasks.all()) == {T[2], T[1]}
    assert set(P[3].tasks.all()) == {T[3], T[1]}
    # additionally, all of the projects should have T1
    assert Project.objects.filter(tasks=T[1]).count() == Project.objects.all().count()
    assert_all_projects_are_synced_with_instance_m2m_field(T[1],'catalogs')


    # === Update: (from empty) add C1 to T1 → it should appear in P1 only again ===
    T[1].catalogs.add(C[1])  # T1 → [C1]

    assert set(P[1].tasks.all()) == {T[1]}
    assert set(P[2].tasks.all()) == {T[2]}
    assert set(P[3].tasks.all()) == {T[3]}
    assert_all_projects_are_synced_with_instance_m2m_field(T[1],'catalogs')

    # === Update: set [C1, C2] to T1 → it should appear in P1, P2 ===
    T[1].catalogs.set([C[1], C[2]])  # T1 → [C1, C2]

    assert set(P[1].tasks.all()) == {T[1]}  # should remain unchanged
    assert set(P[2].tasks.all()) == {T[2], T[1]}
    assert set(P[3].tasks.all()) == {T[3]}

    # === Update: set T1 to [C2] → should be removed from P1 ===
    T[1].catalogs.set([C[2]])
    assert set(P[1].tasks.all()) == set()  # removed
    assert set(P[2].tasks.all()) == {T[2], T[1]}  # stays
    assert set(P[3].tasks.all()) == {T[3]}
    assert_all_projects_are_synced_with_instance_m2m_field(T[2],'catalogs')

    # === Update: remove C2 and add C3 to T1 → it should appear in P3 ===
    T[1].catalogs.remove(C[2])  # T1 → []
    T[1].catalogs.add(C[3])  # T1 → [C3]

    assert set(P[1].tasks.all()) == set()
    assert set(P[2].tasks.all()) == {T[2]}
    assert set(P[3].tasks.all()) == {T[3], T[1]}  # got T1
    assert_all_projects_are_synced_with_instance_m2m_field(T[3],'catalogs')

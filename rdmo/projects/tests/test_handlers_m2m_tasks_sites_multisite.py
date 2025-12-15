import pytest

from rdmo.projects.models import Project
from rdmo.projects.tests.helpers.project_sync.arrange_project_tasks import arrange_projects_sites_and_tasks
from rdmo.projects.tests.helpers.project_sync.assert_project_views_or_tasks import (
    assert_all_projects_are_synced_with_instance_m2m_field,
)

pytestmark = pytest.mark.usefixtures("enable_multisite")


@pytest.mark.django_db
def test_project_tasks_sync_when_updating_task_sites_multisite(settings, enable_project_tasks_sync):
    assert settings.PROJECT_TASKS_SYNC
    assert settings.MULTISITE  # just a double-check

    P, T, S = arrange_projects_sites_and_tasks()
    # === Initial state ===
    # P1 (with S1) has T1, etc...
    assert set(P[1].tasks.all()) == {T[1]}
    assert set(P[2].tasks.all()) == {T[2]}
    assert set(P[3].tasks.all()) == {T[3]}

    # === Update: T1 has no sites → with MULTISITE=True it should appear in NO projects ===
    T[1].sites.clear()

    assert set(P[1].tasks.all()) == set()
    assert set(P[2].tasks.all()) == {T[2]}
    assert set(P[3].tasks.all()) == {T[3]}
    assert Project.objects.filter(tasks=T[1]).count() == 0

    # === Update: (from empty) add S1 to T1 → it should appear in P1 only again ===
    T[1].sites.add(S[1])  # T1 → [S1]

    assert set(P[1].tasks.all()) == {T[1]}
    assert set(P[2].tasks.all()) == {T[2]}
    assert set(P[3].tasks.all()) == {T[3]}
    # helper works fine again as soon as instance.sites is non-empty
    assert_all_projects_are_synced_with_instance_m2m_field(T[1], 'sites')

    # === Update: set [S1, S2] to T1 → it should appear in P1, P2 ===
    T[1].sites.set([S[1], S[2]])  # T1 → [S1, S2]

    assert set(P[1].tasks.all()) == {T[1]}  # should remain unchanged
    assert set(P[2].tasks.all()) == {T[2], T[1]}
    assert set(P[3].tasks.all()) == {T[3]}
    assert_all_projects_are_synced_with_instance_m2m_field(T[1], 'sites')

    # === Update: set T1 to [S2] → should be removed from P1 ===
    T[1].sites.set([S[2]])

    assert set(P[1].tasks.all()) == set()  # removed
    assert set(P[2].tasks.all()) == {T[2], T[1]}  # stays
    assert set(P[3].tasks.all()) == {T[3]}
    assert_all_projects_are_synced_with_instance_m2m_field(T[1], 'sites')

    # === Update: remove S2 and add S3 to T1 → it should appear in P3 only ===
    T[1].sites.remove(S[2])  # T1 → []
    T[1].sites.add(S[3])  # T1 → [S3]

    assert set(P[1].tasks.all()) == set()
    assert set(P[2].tasks.all()) == {T[2]}
    assert set(P[3].tasks.all()) == {T[3], T[1]}  # got T1
    assert_all_projects_are_synced_with_instance_m2m_field(T[3], 'sites')

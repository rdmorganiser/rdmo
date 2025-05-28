import pytest

from django.contrib.sites.models import Site

from rdmo.projects.models import Project
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task

from .helpers import assert_all_projects_are_synced_with_instance_catalogs, enable_project_tasks_sync  # noqa: F401

P_TITLE = "Sync P{}"
one_two_three = (1, 2, 3)

@pytest.mark.django_db
def test_project_tasks_sync_when_updating_task_catalogs(settings, enable_project_tasks_sync):  # noqa:F811
    assert settings.PROJECT_TASKS_SYNC
    site_1 = Site.objects.get(id=1)

    # Arrange: the project, catalog and task objects
    # all catalogs and tasks should have available=True
    # P1, P2, P3
    P = {
        n: Project.objects.create(
            title=P_TITLE.format(n),
            catalog=Catalog.objects.get(id=n), site=site_1)
        for n in one_two_three
    }
    C = {n: P[n].catalog for n in one_two_three}  # C1, C2, C3
    T = {n: Task.objects.get(id=n) for n in one_two_three}  # T1, T2, T3

    # Arrange the catalogs
    for catalog in C.values():
        catalog.available = True
        catalog.sites.clear()
        catalog.groups.clear()
        catalog.save()

    # Set a certain initial state for the project.tasks
    # this is a sort of random state
    P[1].tasks.set([T[1], T[2], T[3]])
    P[2].tasks.clear()
    P[3].tasks.set([T[3]])

    # Clear everything to reset state for the tasks.catalogs
    # which will also affect the project.tasks
    for n, task in T.items():
        task.available = True
        task.sites.clear()
        task.groups.clear()
        task.catalogs.set([C[n]])
        task.save()

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
    assert_all_projects_are_synced_with_instance_catalogs(T[1])


    # === Update: (from empty) add C1 to T1 → it should appear in P1 only again ===
    T[1].catalogs.add(C[1])  # T1 → [C1]

    assert set(P[1].tasks.all()) == {T[1]}
    assert set(P[2].tasks.all()) == {T[2]}
    assert set(P[3].tasks.all()) == {T[3]}
    assert_all_projects_are_synced_with_instance_catalogs(T[1])

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
    assert_all_projects_are_synced_with_instance_catalogs(T[2])

    # === Update: remove C2 and add C3 to T1 → it should appear in P3 ===
    T[1].catalogs.remove(C[2])  # T1 → []
    T[1].catalogs.add(C[3])  # T1 → [C3]

    assert set(P[1].tasks.all()) == set()
    assert set(P[2].tasks.all()) == {T[2]}
    assert set(P[3].tasks.all()) == {T[3], T[1]}  # got T1
    assert_all_projects_are_synced_with_instance_catalogs(T[3])

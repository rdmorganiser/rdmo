import pytest

from rdmo.projects.tests.helpers.project_sync.arrange_project_tasks import arrange_projects_catalogs_and_tasks


@pytest.mark.django_db
def test_project_tasks_sync_when_updating_available_on_a_task(settings, enable_project_tasks_sync):
    assert settings.PROJECT_TASKS_SYNC

    P, C, T = arrange_projects_catalogs_and_tasks()
    # === Initial state ===
    # P1 (with C1) has V1, etc..
    assert set(P[1].tasks.all()) == {T[1]}
    assert set(P[2].tasks.all()) == {T[2]}
    assert set(P[3].tasks.all()) == {T[3]}
    # Arrange: make V1 unavailable
    T[1].available = False
    T[1].save()

    # === Act: V1 is unavailable and has no catalogs → it should not appear in any projects ===
    T[1].catalogs.clear()
    assert set(P[1].tasks.all()) == set()  # should be removed
    assert set(P[2].tasks.all()) == {T[2]}
    assert set(P[3].tasks.all()) == {T[3]}

    # === Act: V1 is unavailable and is added to catalogs → it should not appear in any projects ===
    T[1].catalogs.set([C[1], C[2]])  # V1 → [C1, C2]
    assert set(P[1].tasks.all()) == set() # should stay empty
    assert set(P[2].tasks.all()) == {T[2]}
    assert set(P[3].tasks.all()) == {T[3]}

    # === Act: make V1 available → it should appear in projects P1,P2 ===
    T[1].available = True
    T[1].save(update_fields=['available'])

    assert set(P[1].tasks.all()) == {T[1]}
    assert set(P[2].tasks.all()) == {T[2], T[1]}
    assert set(P[3].tasks.all()) == {T[3]}

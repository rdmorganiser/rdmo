import pytest

from rdmo.projects.tests.helpers.project_sync.arrange_project_views import arrange_projects_catalogs_and_views


@pytest.mark.django_db
def test_project_views_sync_when_updating_available_on_a_view(settings, enable_project_views_sync):
    assert settings.PROJECT_VIEWS_SYNC

    P, C, V = arrange_projects_catalogs_and_views()
    # === Initial state ===
    # P1 (with C1) has V1, etc..
    assert set(P[1].views.all()) == {V[1]}
    assert set(P[2].views.all()) == {V[2]}
    assert set(P[3].views.all()) == {V[3]}
    # Arrange: make V1 unavailable
    V[1].available = False
    V[1].save()

    # === Act: V1 is unavailable and has no catalogs → it should not appear in any projects ===
    V[1].catalogs.clear()
    assert set(P[1].views.all()) == set()  # should be removed
    assert set(P[2].views.all()) == {V[2]}
    assert set(P[3].views.all()) == {V[3]}

    # === Act: V1 is unavailable and is added to catalogs → it should not appear in any projects ===
    V[1].catalogs.set([C[1], C[2]])  # V1 → [C1, C2]
    assert set(P[1].views.all()) == set() # should stay empty
    assert set(P[2].views.all()) == {V[2]}
    assert set(P[3].views.all()) == {V[3]}

    # === Act: make V1 available → it should appear in projects P1,P2 ===
    V[1].available = True
    V[1].save(update_fields=['available'])

    assert set(P[1].views.all()) == {V[1]}
    assert set(P[2].views.all()) == {V[2], V[1]}
    assert set(P[3].views.all()) == {V[3]}

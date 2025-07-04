import pytest

from rdmo.projects.models import Project
from rdmo.projects.tests.helpers.project_sync.arrange_project_views import arrange_projects_sites_and_views
from rdmo.projects.tests.helpers.project_sync.assert_project_views_or_tasks import (
    assert_all_projects_are_synced_with_instance_m2m_field,
)


@pytest.mark.django_db
def test_project_views_sync_when_updating_view_sites(settings, enable_project_views_sync):
    assert settings.PROJECT_VIEWS_SYNC

    P, V, S = arrange_projects_sites_and_views()
    # === Initial state ===
    # P1 (with C1) has V1, etc...
    assert set(P[1].views.all()) == {V[1]}
    assert set(P[2].views.all()) == {V[2]}
    assert set(P[3].views.all()) == {V[3]}

    # === Update: V1 has no catalogs → it should appear in all projects ===
    V[1].sites.clear()
    assert set(P[1].views.all()) == {V[1]}  # should remain unchanged
    assert set(P[2].views.all()) == {V[2], V[1]}
    assert set(P[3].views.all()) == {V[3], V[1]}
    # additionally, all of the projects should have T1
    assert Project.objects.filter(views=V[1]).count() == Project.objects.all().count()
    assert_all_projects_are_synced_with_instance_m2m_field(V[1], 'sites')

    # === Update: (from empty) add C1 to V1 → it should appear in P1 only again ===
    V[1].sites.add(S[1])  # V1 → [C1]

    assert set(P[1].views.all()) == {V[1]}
    assert set(P[2].views.all()) == {V[2]}
    assert set(P[3].views.all()) == {V[3]}
    assert_all_projects_are_synced_with_instance_m2m_field(V[1], 'sites')

    # === Update: set [C1, C2] to V1 → it should appear in P1, P2 ===
    V[1].sites.set([S[1], S[2]])  # V1 → [C1, C2]

    assert set(P[1].views.all()) == {V[1]}  # should remain unchanged
    assert set(P[2].views.all()) == {V[2], V[1]}
    assert set(P[3].views.all()) == {V[3]}

    # === Update: set V1 to [C2] → should be removed from P1 ===
    V[1].sites.set([S[2]])
    assert set(P[1].views.all()) == set()  # removed
    assert set(P[2].views.all()) == {V[2], V[1]}  # stays
    assert set(P[3].views.all()) == {V[3]}
    assert_all_projects_are_synced_with_instance_m2m_field(V[2], 'sites')

    # === Update: remove C2 and add C3 to V1 → it should appear in P1 and P3 ===
    V[1].sites.remove(S[2])  # V1 → []
    V[1].sites.add(S[3])  # V1 → [C3]

    assert set(P[1].views.all()) == set()
    assert set(P[2].views.all()) == {V[2]}
    assert set(P[3].views.all()) == {V[3], V[1]}  # got V1
    assert_all_projects_are_synced_with_instance_m2m_field(V[3], 'sites')

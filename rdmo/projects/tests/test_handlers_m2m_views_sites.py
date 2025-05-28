import pytest

from django.contrib.sites.models import Site

from rdmo.projects.models import Project
from rdmo.questions.models import Catalog
from rdmo.views.models import View

from .helpers import assert_all_projects_are_synced_with_instance_m2m_field, enable_project_views_sync  # noqa: F401

P_TITLE = "Sync P{}"  # title of newly created test projects
one_two_three = (1, 2, 3)  # will be used for creating P1, V1, C1, P2, ..etc.


@pytest.mark.django_db
def test_project_views_sync_when_updating_view_sites(settings, enable_project_views_sync):  # noqa:F811
    assert settings.PROJECT_VIEWS_SYNC

    # Arrange: the project, catalog and view objects
    # all catalogs and views should have available=True
    # P1, P2, P3
    S = {n: Site.objects.get(id=n) for n in one_two_three}  # S1, S2, S3
    C = {n: Catalog.objects.get(id=n) for n in one_two_three}  # C1, C2, C3
    V = {n: View.objects.get(id=n) for n in one_two_three}  # V1, V2, V3
    P = {
        n: Project.objects.create(
            title=P_TITLE.format(n),
            catalog=C[n],
            site=S[n],
        )
        for n in one_two_three
    }

    # Arrange the catalogs
    for catalog in C.values():
        catalog.available = True
        catalog.sites.clear()
        catalog.groups.clear()
        catalog.save()

    # Set a certain initial state for the project.views
    # this is a sort of random state
    P[1].views.set([V[1],V[2],V[3]])
    P[2].views.clear()
    P[3].views.set([V[3]])

    # Clear everything to reset state for the views.catalogs
    # which will also affect the project.views
    for n, view in V.items():
        view.available = True
        view.catalogs.clear()
        view.groups.clear()
        view.sites.set([S[n]])
        view.save()

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

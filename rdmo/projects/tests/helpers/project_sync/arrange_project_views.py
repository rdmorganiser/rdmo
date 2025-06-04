from django.contrib.sites.models import Site

from rdmo.projects.models import Project
from rdmo.questions.models import Catalog
from rdmo.views.models import View

P_TITLE = "Sync P{}"  # title of newly created test projects
one_two_three = (1, 2, 3)  # will be used for creating P1, V1, C1, P2, ..etc.

def arrange_projects_catalogs_and_views():

    # Arrange: the project, catalog and view objects
    # all catalogs and views should have available=True
    C = {n: Catalog.objects.get(id=n) for n in one_two_three}  # C1, C2, C3
    V = {n: View.objects.get(id=n) for n in one_two_three}  # V1, V2, V3
    P = {  # P1, P2, P3
        n: Project.objects.create(
            title=P_TITLE.format(n),
            catalog=C[n],
            site=Site.objects.get(id=1)
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
        view.sites.clear()
        view.groups.clear()
        view.catalogs.set([C[n]])
        view.save()

    return P, C, V


def arrange_projects_sites_and_views():
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
    P[1].views.set([V[1], V[2], V[3]])
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

    return P, V, S

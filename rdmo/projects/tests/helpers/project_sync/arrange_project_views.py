from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site

from rdmo.projects.models import Membership, Project
from rdmo.projects.tests.helpers.project_sync.constants import P_TITLE, one_two_three
from rdmo.questions.models import Catalog
from rdmo.views.models import View


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
        catalog.save()
        catalog.sites.clear()
        catalog.groups.clear()

    # Set a certain initial state for the project.views
    # this is a sort of random state
    P[1].views.set([V[1],V[2],V[3]])
    P[2].views.clear()
    P[3].views.set([V[3]])

    # Clear everything to reset state for the views.catalogs
    # which will also affect the project.views
    for n, view in V.items():
        view.available = True
        view.save()
        view.sites.clear()
        view.groups.clear()
        view.catalogs.set([C[n]])

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
        catalog.save()
        catalog.sites.clear()
        catalog.groups.clear()

    # Set a certain initial state for the project.views
    # this is a sort of random state
    P[1].views.set([V[1], V[2], V[3]])
    P[2].views.clear()
    P[3].views.set([V[3]])

    # Clear everything to reset state for the views.catalogs
    # which will also affect the project.views
    for n, view in V.items():
        view.available = True
        view.save()
        view.catalogs.clear()
        view.groups.clear()
        view.sites.set([S[n]])

    return P, V, S


def arrange_projects_groups_and_views():
    # Arrange: the project, catalog and view objects
    # all catalogs and views should have available=True
    S = {n: Site.objects.get(id=1) for n in one_two_three}  # S1, S2, S3
    C = {n: Catalog.objects.get(id=1) for n in one_two_three}  # C1, C2, C3
    V = {n: View.objects.get(id=n) for n in one_two_three}  # V1, V2, V3
    P = {  # P1, P2, P3
        n: Project.objects.create(
            title=P_TITLE.format(n),
            catalog=C[n],
            site=S[n],
        )
        for n in one_two_three
    }
    # Create groups, users and project memberships
    G = {n: Group.objects.create(name=f"Sync G{n}") for n in one_two_three}
    for n in one_two_three:
        _user = User.objects.create(username=f"Sync U{n}")
        _user.groups.set([G[n]])
        # this sets P[1].groups -> U[n].groups
        Membership.objects.create(user_id=_user.id, project_id=P[n].id, role='owner')

    # Arrange the catalogs
    for catalog in C.values():
        catalog.available = True
        catalog.save()
        catalog.sites.clear()
        catalog.groups.clear()

    # Set a certain initial state for the project.views
    # this is a sort of random state
    P[1].views.set([V[1], V[2], V[3]])
    P[2].views.clear()
    P[3].views.set([V[3]])

    # Clear everything to reset state for the views.groups
    # -> this will also affect the project.views
    for n, view in V.items():
        view.available = True
        view.save()
        view.catalogs.clear()
        view.sites.clear()
        view.groups.set([G[n]])  # set groups as last so that will be state

    return P, V , G

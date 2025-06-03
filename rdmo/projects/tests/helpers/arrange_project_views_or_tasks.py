from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site

from rdmo.projects.models import Membership, Project
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
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


def arrange_projects_catalogs_and_tasks():
    # Arrange: the project, catalog and view objects
    # all catalogs and views should have available=True

    C = {n: Catalog.objects.get(id=n) for n in one_two_three}  # C1, C2, C3
    T = {n: Task.objects.get(id=n) for n in one_two_three}  # T1, T2, T3
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

    return P, C, T


def arrange_projects_sites_and_views_or_tasks():
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


def arrange_projects_groups_and_views_or_tasks():
    # Arrange: the project, catalog and view objects
    # all catalogs and views should have available=True
    # P1, P2, P3
    S = {n: Site.objects.get(id=1) for n in one_two_three}  # S1, S2, S3
    C = {n: Catalog.objects.get(id=1) for n in one_two_three}  # C1, C2, C3
    V = {n: View.objects.get(id=n) for n in one_two_three}  # V1, V2, V3
    P = {
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
        catalog.sites.clear()
        catalog.groups.clear()
        catalog.save()

    # Clear everything to reset state for the views.groups
    # -> this will also affect the project.views
    for n, view in V.items():
        view.available = True
        view.save()
        view.catalogs.clear()
        view.sites.clear()
        view.groups.set([G[n]])  # set groups as last so that will be state

    # Set a certain initial state for the project.views
    # this is a sort of random state
    P[1].views.set([V[1], V[2], V[3]])
    P[2].views.clear()
    P[3].views.set([V[3]])

    return P, V , G

from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site

from rdmo.projects.models import Membership, Project
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task

from .constants import P_TITLE, one_two_three


def arrange_projects_catalogs_and_tasks():
    # Arrange: the project, catalog and task objects
    # all catalogs and tasks should have available=True
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

def arrange_projects_sites_and_tasks():
    # Arrange: the project, catalog and task objects
    # all catalogs and tasks should have available=True
    # P1, P2, P3
    S = {n: Site.objects.get(id=n) for n in one_two_three}  # S1, S2, S3
    C = {n: Catalog.objects.get(id=n) for n in one_two_three}  # C1, C2, C3
    T = {n: Task.objects.get(id=n) for n in one_two_three}  # T1, T2, T3
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

    # Set a certain initial state for the project.tasks
    # this is a sort of random state
    P[1].tasks.set([T[1], T[2], T[3]])
    P[2].tasks.clear()
    P[3].tasks.set([T[3]])

    # Clear everything to reset state for the tasks.catalogs
    # which will also affect the project.tasks
    for n, task in T.items():
        task.available = True
        task.catalogs.clear()
        task.groups.clear()
        task.sites.set([S[n]])
        task.save()

    return P, T, S

def arrange_projects_groups_and_tasks():
    # Arrange: the project, catalog and task objects
    # all catalogs and tasks should have available=True
    S = {n: Site.objects.get(id=1) for n in one_two_three}  # S1, S2, S3
    C = {n: Catalog.objects.get(id=1) for n in one_two_three}  # C1, C2, C3
    T = {n: Task.objects.get(id=n) for n in one_two_three}  # T1, T2, T3
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
        catalog.sites.clear()
        catalog.groups.clear()
        catalog.save()

    # Set a certain initial state for the project.tasks
    # this is a sort of random state
    P[1].tasks.set([T[1], T[2], T[3]])
    P[2].tasks.clear()
    P[3].tasks.set([T[3]])

    # Clear everything to reset state for the tasks.groups
    # -> this will also affect the project.tasks
    for n, task in T.items():
        task.available = True
        task.save()
        task.catalogs.clear()
        task.sites.clear()
        task.groups.set([G[n]])  # set groups as last so that will be state

    return P, T , G

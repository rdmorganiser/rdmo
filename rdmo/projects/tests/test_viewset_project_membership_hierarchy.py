import pytest

from django.urls import reverse

from ..models import Project

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('api', 'api'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

view_membership_permission_map = {
    'owner': [1, 2, 3, 4, 5, 12],
    'manager': [1, 3, 5, 12],
    'author': [1, 3, 5, 12],
    'guest': [1, 3, 5, 12],
    'user': [12],
    'api': [1, 2, 3, 4, 5, 12],
    'site': [1, 2, 3, 4, 5, 12]
}

urlnames = {
    'hierarchy': 'v1-projects:project-membership-hierarchy'
}

projects = [1, 2, 3, 4, 5, 12]

project_memberships = {
    3: {5},
    4: {5},
    5: {5, 6, 7, 8}
}


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_hierarchy(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['hierarchy'], args=[project_id])
    response = client.get(url)

    if project_id in view_membership_permission_map.get(username, []):
        assert response.status_code == 200
        assert {m['user']['id'] for m in response.json()} == project_memberships.get(project_id, set())
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', [('owner', 'owner'), ('guest', 'guest')])
def test_hierarchy_without_catalog(db, client, username, password):
    project = Project.objects.get(pk=1)
    project.catalog.delete()
    project.refresh_from_db()

    client.login(username=username, password=password)
    url = reverse(urlnames['hierarchy'], args=[project.pk])
    response = client.get(url)

    assert response.status_code == 200

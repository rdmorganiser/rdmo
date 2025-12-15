import pytest

from django.urls import reverse

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

view_project_catalog_permission_map = {  # id, available
    'owner': [(1, True)],
    'manager': [(1, True)],
    'author': [(1, True)],
    'guest': [(1, True)],
    'user': [(1, True)],
    'editor': [(1, True)],
    'reviewer': [(1, True)],
    'api': [(1, True),(2, False)],
    'site': [(1, True)]
}

urlnames = {
    'list': 'v1-projects:catalog-list',
}

other_sites_catalogs = [(3, True), (4, True)]

@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)

    if password:
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert view_project_catalog_permission_map[username] == [(i['id'],i['available']) for i in data]
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
def test_list_with_cleared_sites(db, client, clear_sites_from_other_catalogs, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)

    if password:
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        catalogs = view_project_catalog_permission_map[username] + other_sites_catalogs
        if any(not available for _id,available in catalogs):  # api sees an available=False catalog
            catalogs = sorted(
                catalogs,
                key=lambda i: (not i[1], i[0]),
            )
        assert catalogs == [(i['id'],i['available']) for i in data]
    else:
        assert response.status_code == 401

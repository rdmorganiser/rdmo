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

urlnames = {
    'list': 'v1-projects:catalog-list',
    'detail': 'v1-projects:catalog-detail'
}

catalogs = [1, 2]


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)

    if password:
        assert response.status_code == 200
    else:
        assert response.status_code == 401
    if password:
        assert response.status_code == 200
        assert sorted([item['id'] for item in response.json()]) == catalogs
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('catalog_id', catalogs)
def test_detail(db, client, username, password, catalog_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[catalog_id])
    response = client.get(url)

    if password:
        assert response.status_code == 200
        assert response.json().get('id') == catalog_id
    else:
        assert response.status_code == 401

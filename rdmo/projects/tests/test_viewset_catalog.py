import pytest

from django.contrib.sites.models import Site
from django.urls import reverse

from rdmo.questions.models import Catalog

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
    'user': 'v1-projects:catalog-user'
}

catalog_id = 1


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)

    if password:
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        data = response.json()
        site = Site.objects.get_current()
        catalogs = Catalog.objects.filter(sites=site)

        assert {c['id'] for c in data} == {c.id for c in catalogs}
        assert {c['available'] for c in data} == {c.available for c in catalogs}
    else:
        assert response.status_code == 401

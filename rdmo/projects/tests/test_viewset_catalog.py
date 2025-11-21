import pytest

from django.contrib.auth import get_user_model
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
    'user': 'v1-projects:catalog-user'  # does not exist
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
        user = get_user_model().objects.get(username=username)
        catalogs = Catalog.objects.for_projects_view(user)
        assert {c['id'] for c in data} == set(catalogs.values_list('id', flat=True))
        assert {c['available'] for c in data} == set(catalogs.values_list('available', flat=True))

    else:
        assert response.status_code == 401

import pytest

from django.urls import reverse

from rdmo.projects.constants import ROLE_CHOICES

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
    'list': 'v1-projects:role-list'
}


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)

    if password:
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert tuple([(role['id'], role['text']) for role in response.json()]) == ROLE_CHOICES
    else:
        assert response.status_code == 401

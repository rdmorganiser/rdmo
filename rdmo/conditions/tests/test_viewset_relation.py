import pytest
from django.urls import reverse

users = (
    ('anonymous', None),
    ('user', 'user'),
    ('site', 'site'),
)

groups = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('api', 'api'),
)

status_map = {
    'list': {
        'site': 200, 'user': 200, 'anonymous': 401
    }
}

urlnames = {
    'list': 'v1-conditions:relation-list',
}


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()

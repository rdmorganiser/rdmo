import pytest

from django.urls import reverse

users = (
    'owner',
    'manager',
    'author',
    'guest',
    'admin',
    'api',
    'site',
    'user',
    'anonymous',
)

urlnames = {
    'list': 'v1-projects:export-list'
}

plugin_keys = [
    'xml',
    'csvcomma',
    'csvsemicolon',
    'json',
    'set',
    'oauth',
]

@pytest.mark.parametrize('username', users)
def test_list(db, client, login, username):
    login(username)

    url = reverse(urlnames['list'])
    response = client.get(url)

    if username == 'anonymous':
        assert response.status_code == 401
    else:
        assert response.status_code == 200
        assert list(response.json().keys()) == plugin_keys

        assert response.json()['xml']['label']
        assert response.json()['xml']['description']
        assert response.json()['xml']['download'] is True

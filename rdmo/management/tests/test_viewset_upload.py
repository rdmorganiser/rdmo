from pathlib import Path

import pytest
from django.conf import settings
from django.urls import reverse

users = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('api', 'api'),
    ('anonymous', None),
)

status_map = {
    'list': {
        'editor': 405, 'reviewer': 405, 'api': 405, 'user': 405, 'anonymous': 401
    },
    'create': {
        'editor': 200, 'reviewer': 403, 'api': 200, 'user': 403, 'anonymous': 401
    },
    'create_error': {
        'editor': 400, 'reviewer': 400, 'api': 400, 'user': 400, 'anonymous': 401
    }
}

urlnames = {
    'list': 'v1-management:upload-list'
}


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'catalogs.xml'

    url = reverse(urlnames['list'])
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'file': f})

    assert response.status_code == status_map['create'][username], response.json()
    if response.status_code == 200:
        for element in response.json():
            assert element.get('imported') is None


@pytest.mark.parametrize('username,password', users)
def test_create_import(db, client, username, password):
    client.login(username=username, password=password)

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'catalogs.xml'

    url = reverse(urlnames['list'])
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'file': f, 'import': 'true'})

    assert response.status_code == status_map['create'][username], response.json()
    if response.status_code == 200:
        for element in response.json():
            assert element.get('imported') is True


@pytest.mark.parametrize('username,password', users)
def test_create_empty(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.post(url, {})
    assert response.status_code == status_map['create_error'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_error(db, client, username, password):
    client.login(username=username, password=password)

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'error.xml'

    url = reverse(urlnames['list'])
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'file': f})

    assert response.status_code == status_map['create_error'][username], response.json()

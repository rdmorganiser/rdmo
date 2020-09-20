import pytest
from django.urls import reverse

from ..models import Integration, Project

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

status_map = {
    'create_get': {
        'owner': 200, 'manager': 200, 'author': 403, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'create_post': {
        'owner': 302, 'manager': 302, 'author': 403, 'guest': 403, 'user': 403, 'site': 302, 'anonymous': 302
    },
    'update_get': {
        'owner': 200, 'manager': 200, 'author': 403, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'update_post': {
        'owner': 302, 'manager': 302, 'author': 403, 'guest': 403, 'user': 403, 'site': 302, 'anonymous': 302
    },
    'delete_get': {
        'owner': 200, 'manager': 200, 'author': 403, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'delete_post': {
        'owner': 302, 'manager': 302, 'author': 403, 'guest': 403, 'user': 403, 'site': 302, 'anonymous': 302
    }
}

urlnames = {
    'create': 'integration_create',
    'update': 'integration_update',
    'delete': 'integration_delete',
}

project_pk = 1
integration_pk = 1


@pytest.mark.parametrize('username,password', users)
def test_integration_create_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['create'], args=[project_pk, 'github'])
    response = client.get(url)
    assert response.status_code == status_map['create_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_integration_create_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['create'], args=[project_pk, 'github'])
    data = {
        'repo': 'example/example1'
    }
    response = client.post(url, data)
    assert response.status_code == status_map['create_post'][username], response.content
    if password and response.status_code == 302:
        assert Integration.objects.exclude(pk=integration_pk).first().options_dict == {
            'repo': 'example/example1'
        }


@pytest.mark.parametrize('username,password', users)
def test_integration_update_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update'], args=[project_pk, integration_pk])
    response = client.get(url)
    assert response.status_code == status_map['update_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_integration_update_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update'], args=[project_pk, integration_pk])
    data = {
        'repo': 'example/example2'
    }
    response = client.post(url, data)
    assert response.status_code == status_map['update_post'][username], response.content
    if password and response.status_code == 302:
        assert Integration.objects.first().options_dict == {
            'repo': 'example/example2'
        }


@pytest.mark.parametrize('username,password', users)
def test_integration_delete_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['delete'], args=[project_pk, integration_pk])
    response = client.get(url)
    assert response.status_code == status_map['delete_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_integration_delete_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['delete'], args=[project_pk, integration_pk])
    response = client.delete(url)
    assert response.status_code == status_map['delete_post'][username], response.content
    if password and response.status_code == 302:
        assert Integration.objects.first() is None

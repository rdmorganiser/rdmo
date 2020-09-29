import hmac
import json

import pytest
from django.urls import reverse

from ..models import Integration, Issue

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
    'webhook': 'integration_webhook'
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
        values = Integration.objects.exclude(pk=integration_pk).first().options.values('key', 'value', 'secret')
        assert sorted(values, key=lambda obj: obj['key']) == [
            {
                'key': 'repo',
                'value': 'example/example1',
                'secret': False
            },
            {
                'key': 'secret',
                'value': '',
                'secret': True
            }
        ]


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
        'repo': 'example/example2',
        'secret': 'super_secret'
    }
    response = client.post(url, data)
    assert response.status_code == status_map['update_post'][username], response.content
    if password and response.status_code == 302:
        values = Integration.objects.first().options.values('key', 'value', 'secret')
        assert sorted(values, key=lambda obj: obj['key']) == [
            {
                'key': 'repo',
                'value': 'example/example2',
                'secret': False
            },
            {
                'key': 'secret',
                'value': 'super_secret',
                'secret': True
            }
        ]


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


@pytest.mark.parametrize('username,password', users)
def test_integration_webhook_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['webhook'], args=[project_pk, integration_pk])
    response = client.get(url)
    assert response.status_code == 405
    assert Issue.objects.first().status == 'open'


@pytest.mark.parametrize('username,password', users)
def test_integration_webhook_post(db, client, username, password):
    client.login(username=username, password=password)

    secret = 'super_duper_secret'
    url = reverse(urlnames['webhook'], args=[project_pk, integration_pk])
    data = {
        'action': 'closed',
        'issue': {
            'html_url': 'https://github.com/example/example/issues/1'
        }
    }
    body = json.dumps(data)
    signature = 'sha1=' + hmac.new(secret.encode(), body.encode(), 'sha1').hexdigest()

    response = client.post(url, data, **{'HTTP_X_HUB_SIGNATURE': signature, 'content_type': 'application/json'})
    assert response.status_code == 200
    assert Issue.objects.first().status == 'closed'


@pytest.mark.parametrize('username,password', users)
def test_integration_webhook_post_no_secret(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['webhook'], args=[project_pk, integration_pk])
    response = client.post(url, {})
    assert response.status_code == 404
    assert Issue.objects.first().status == 'open'

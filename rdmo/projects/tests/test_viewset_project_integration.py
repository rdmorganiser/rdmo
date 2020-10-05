import json

import pytest
from django.urls import reverse

from ..models import Integration

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

status_map = {
    'list': {
        'owner': 200, 'manager': 200, 'author': 404, 'guest': 404, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 404
    },
    'detail': {
        'owner': 200, 'manager': 200, 'author': 404, 'guest': 404, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 404
    },
    'create': {
        'owner': 201, 'manager': 201, 'author': 404, 'guest': 404, 'api': 201, 'user': 404, 'site': 201, 'anonymous': 404
    },
    'update': {
        'owner': 200, 'manager': 200, 'author': 404, 'guest': 404, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 404
    },
    'delete': {
        'owner': 204, 'manager': 204, 'author': 404, 'guest': 404, 'api': 204, 'user': 404, 'site': 204, 'anonymous': 404
    }
}

urlnames = {
    'list': 'v1-projects:project-integration-list',
    'detail': 'v1-projects:project-integration-detail'
}

site_id = 1
project_id = 1


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()
    if response.status_code == 200:
        assert isinstance(response.json(), list)
        assert len(response.json()) == 1


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)

    instances = Integration.objects.filter(project_id=project_id)
    for instance in instances:
        url = reverse(urlnames['detail'], args=[project_id, instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()
        if response.status_code == 200:
            assert response.json().get('id') == instance.id


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'provider_key': 'github',
        'options': [
            {
                'key': 'repo',
                'value': 'example/example'
            }
        ]
    }

    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_error1(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'provider_key': 'wrong',
        'options': [
            {
                'key': 'repo',
                'value': 'example/example'
            }
        ]
    }

    response = client.post(url, data=json.dumps(data), content_type="application/json")

    if status_map['create'][username] == 201:
        assert response.status_code == 400, response.json()
        assert response.json()['provider_key'], response.json()
    else:
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_error2(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'provider_key': 'github',
        'options': [
            {
                'key': 'repo',
                'value': ''
            }
        ]
    }

    response = client.post(url, data=json.dumps(data), content_type="application/json")

    if status_map['create'][username] == 201:
        assert response.status_code == 400, response.json()
        assert response.json()['options'][0]['value'], response.json()
    else:
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_error3(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'provider_key': 'github',
        'options': [
            {
                'key': 'repo',
                'value': 'example/example'
            },
            {
                'key': 'foo',
                'value': 'bar'
            }
        ]
    }

    response = client.post(url, data=json.dumps(data), content_type="application/json")

    if status_map['create'][username] == 201:
        assert response.status_code == 400, response.json()
        assert 'foo' in response.json()['options'][0], response.json()
    else:
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)

    instances = Integration.objects.filter(project_id=project_id)
    for instance in instances:
        url = reverse(urlnames['detail'], args=[project_id, instance.pk])
        data = {
            'provider_key': 'github',
            'options': [
                {
                    'key': 'repo',
                    'value': 'example/test'
                }
            ]
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()
        if response.status_code == 200:
            assert sorted(response.json().get('options'), key=lambda obj: obj['key']) == [
                {
                    'key': 'repo',
                    'value': 'example/test'
                },
                {
                    'key': 'secret',
                    'value': ''
                }
            ]


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)

    instances = Integration.objects.filter(project_id=project_id)
    for instance in instances:
        url = reverse(urlnames['detail'], args=[project_id, instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.content

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

view_integration_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'guest': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

add_integration_permission_map = change_integration_permission_map = delete_integration_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

urlnames = {
    'list': 'v1-projects:project-integration-list',
    'detail': 'v1-projects:project-integration-detail'
}

projects = [1, 2, 3, 4, 5]
integrations = [1, 2]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_list(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    response = client.get(url)

    if project_id in view_integration_permission_map.get(username, []):
        assert response.status_code == 200

        if username == 'user':
            assert sorted([item['id'] for item in response.json()]) == []
        else:
            values_list = Integration.objects.filter(project_id=project_id) \
                                             .order_by('id').values_list('id', flat=True)
            assert sorted([item['id'] for item in response.json()]) == list(values_list)
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('integration_id', integrations)
def test_detail(db, client, username, password, project_id, integration_id):
    client.login(username=username, password=password)
    integration = Integration.objects.filter(project_id=project_id, id=integration_id).first()

    url = reverse(urlnames['detail'], args=[project_id, integration_id])
    response = client.get(url)

    if integration and project_id in view_integration_permission_map.get(username, []):
        assert response.status_code == 200
        assert response.json().get('id') == integration_id
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_create(db, client, username, password, project_id):
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

    if project_id in add_integration_permission_map.get(username, []):
        assert response.status_code == 201, response.content
    elif project_id in view_integration_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_create_error1(db, client, username, password, project_id):
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

    if project_id in add_integration_permission_map.get(username, []):
        assert response.status_code == 400, response.json()
        assert response.json()['provider_key'], response.json()
    elif project_id in view_integration_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_create_error2(db, client, username, password, project_id):
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

    if project_id in add_integration_permission_map.get(username, []):
        assert response.status_code == 400, response.json()
        assert response.json()['options'][0]['value'], response.json()
    elif project_id in view_integration_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_create_error3(db, client, username, password, project_id):
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

    if project_id in add_integration_permission_map.get(username, []):
        assert response.status_code == 400, response.json()
        assert 'foo' in response.json()['options'][0], response.json()
    elif project_id in view_integration_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('integration_id', integrations)
def test_update(db, client, username, password, project_id, integration_id):
    client.login(username=username, password=password)
    integration = Integration.objects.filter(project_id=project_id, id=integration_id).first()

    url = reverse(urlnames['detail'], args=[project_id, integration_id])
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

    if integration and project_id in change_integration_permission_map.get(username, []):
        assert response.status_code == 200
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
    elif integration and project_id in view_integration_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('integration_id', integrations)
def test_delete(db, client, username, password, project_id, integration_id):
    client.login(username=username, password=password)
    integration = Integration.objects.filter(project_id=project_id, id=integration_id).first()

    url = reverse(urlnames['detail'], args=[project_id, integration_id])
    response = client.delete(url)

    if integration and project_id in delete_integration_permission_map.get(username, []):
        assert response.status_code == 204
    elif integration and project_id in view_integration_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404

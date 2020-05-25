import pytest
from django.urls import reverse

from ..models import Snapshot

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('api', 'api'),
    ('user', 'user'),
    ('anonymous', None),
)

status_map = {
    'list': {
        'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 200, 'user': 403, 'anonymous': 401
    },
    'detail': {
        'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 200, 'user': 403, 'anonymous': 401
    },
    'create': {
        'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 201, 'user': 403, 'anonymous': 401
    },
    'update': {
        'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 200, 'user': 403, 'anonymous': 401
    },
    'delete': {
        'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 405, 'user': 403, 'anonymous': 401
    }
}

urlnames = {
    'list': 'v1-projects:snapshot-list',
    'detail': 'v1-projects:snapshot-detail'
}

project_pk = 1


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Snapshot.objects.filter(project_id=project_pk)

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Snapshot.objects.filter(project_id=project_pk)

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'title': instance.title,
            'description': instance.description
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Snapshot.objects.filter(project_id=project_pk)

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'title': instance.title,
            'description': instance.description
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Snapshot.objects.filter(project_id=project_pk)

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()

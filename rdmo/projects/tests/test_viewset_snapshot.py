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
    ('site', 'site'),
    ('anonymous', None),
)

status_map = {
    'list': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 200, 'site': 200, 'anonymous': 401
    },
    'detail': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 401
    },
    'create': {
        'owner': 405, 'manager': 405, 'author': 405, 'guest': 405, 'api': 405, 'user': 405, 'site': 405, 'anonymous': 401
    },
    'update': {
        'owner': 405, 'manager': 405, 'author': 405, 'guest': 405, 'api': 405, 'user': 405, 'site': 405, 'anonymous': 401
    },
    'delete': {
        'owner': 405, 'manager': 405, 'author': 405, 'guest': 405, 'api': 405, 'user': 405, 'site': 405, 'anonymous': 401
    }
}

urlnames = {
    'list': 'v1-projects:snapshot-list',
    'detail': 'v1-projects:snapshot-detail'
}

site_id = 1
project_id = 1


def assert_snapshot(username, snapshot):
    if username == 'api':
        assert snapshot['id'] in Snapshot.objects.values_list('id', flat=True)
    elif username == 'site':
        assert snapshot['id'] in Snapshot.objects.filter(project__site_id=site_id).values_list('id', flat=True)
    else:
        assert snapshot['id'] in Snapshot.objects.filter(project__user__username=username).values_list('id', flat=True)


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()

    if response.status_code == 200:
        for snapshot in response.json():
            assert_snapshot(username, snapshot)


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Snapshot.objects.filter(project_id=project_id)

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()

        if response == 200:
            assert_snapshot(username, response.json())


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Snapshot.objects.filter(project_id=project_id)

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'title': instance.title,
            'description': instance.description
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()

        if response == 201:
            assert_snapshot(username, response.json())


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Snapshot.objects.filter(project_id=project_id)

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'title': instance.title,
            'description': instance.description
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()

        if response == 200:
            assert_snapshot(username, response.json())


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Snapshot.objects.filter(project_id=project_id)

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()

        if response.status_code == 204:
            assert not Snapshot.objects.filter(pk=instance.pk).exists()
        else:
            assert Snapshot.objects.filter(pk=instance.pk).exists()

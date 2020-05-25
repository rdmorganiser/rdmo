import pytest
from django.urls import reverse

from ..models import Project

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
    'rollback_get': {
        'owner': 200, 'manager': 200, 'author': 403, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'rollback_post': {
        'owner': 302, 'manager': 302, 'author': 403, 'guest': 403, 'user': 403, 'site': 302, 'anonymous': 302
    }
}

urlnames = {
    'create': 'snapshot_create',
    'update': 'snapshot_update',
    'rollback': 'snapshot_rollback'
}

project_id = 1


@pytest.mark.parametrize('username,password', users)
def test_snapshot_create_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['create'], args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['create_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_snapshot_create_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['create'], args=[project_id])
    data = {
        'title': 'A new snapshot',
        'description': 'Some description'
    }
    response = client.post(url, data)
    assert response.status_code == status_map['create_post'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_snapshot_update_get(db, client, username, password):
    client.login(username=username, password=password)
    snapshot = Project.objects.get(pk=project_id).snapshots.first()

    url = reverse(urlnames['update'], args=[project_id, snapshot.pk])
    response = client.get(url)
    assert response.status_code == status_map['update_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_snapshot_update_post(db, client, username, password):
    client.login(username=username, password=password)
    snapshot = Project.objects.get(pk=project_id).snapshots.first()

    url = reverse(urlnames['update'], args=[project_id, snapshot.pk])
    data = {
        'title': snapshot.title,
        'description': snapshot.description
    }
    response = client.post(url, data)
    assert response.status_code == status_map['update_post'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_snapshot_rollback_get(db, client, username, password):
    client.login(username=username, password=password)
    snapshot = Project.objects.get(pk=project_id).snapshots.first()

    url = reverse(urlnames['rollback'], args=[project_id, snapshot.pk])
    response = client.get(url)
    assert response.status_code == status_map['rollback_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_snapshot_rollback_post(db, client, username, password):
    client.login(username=username, password=password)
    snapshot = Project.objects.get(pk=project_id).snapshots.first()

    url = reverse(urlnames['rollback'], args=[project_id, snapshot.pk])
    response = client.post(url)
    assert response.status_code == status_map['rollback_post'][username], response.content

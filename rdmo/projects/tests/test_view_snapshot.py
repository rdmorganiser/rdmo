from pathlib import Path

import pytest
from django.conf import settings
from django.urls import reverse

from rdmo.core.constants import VALUE_TYPE_FILE

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
def test_snapshot_create_post(db, client, files, username, password):
    client.login(username=username, password=password)

    project = Project.objects.get(pk=project_id)
    snapshot_count = project.snapshots.count()
    values_count = project.values.count()
    current_values_count = project.values.filter(snapshot=None).count()

    url = reverse(urlnames['create'], args=[project_id])
    data = {
        'title': 'A new snapshot',
        'description': 'Some description'
    }
    response = client.post(url, data)
    assert response.status_code == status_map['create_post'][username], response.content

    if response.status_code == 302 and password:
        assert project.snapshots.count() == snapshot_count + 1
        assert project.values.count() == values_count + current_values_count
        for file_value in project.values.filter(value_type=VALUE_TYPE_FILE):
            assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()
    else:
        assert project.snapshots.count() == snapshot_count
        assert project.values.count() == values_count


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

    project = Project.objects.get(pk=project_id)
    snapshots = project.snapshots.all()
    snapshot_count = project.snapshots.count()
    values_count = project.values.count()
    values_files = [value.file.name for value in project.values.filter(value_type=VALUE_TYPE_FILE)]

    for snapshot in snapshots:
        url = reverse(urlnames['update'], args=[project_id, snapshot.pk])
        data = {
            'title': snapshot.title,
            'description': snapshot.description
        }
        response = client.post(url, data)
        assert response.status_code == status_map['update_post'][username], response.content

        assert project.snapshots.count() == snapshot_count
        assert project.values.count() == values_count
        for file_value in values_files:
            assert Path(settings.MEDIA_ROOT).joinpath(file_value).exists()


@pytest.mark.parametrize('username,password', users)
def test_snapshot_rollback_get(db, client, username, password):
    client.login(username=username, password=password)
    snapshot = Project.objects.get(pk=project_id).snapshots.first()

    url = reverse(urlnames['rollback'], args=[project_id, snapshot.pk])
    response = client.get(url)
    assert response.status_code == status_map['rollback_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_snapshot_rollback_post(db, client, files, username, password):
    client.login(username=username, password=password)
    snapshot = Project.objects.get(pk=project_id).snapshots.first()

    url = reverse(urlnames['rollback'], args=[project_id, snapshot.pk])
    response = client.post(url)
    assert response.status_code == status_map['rollback_post'][username], response.content

    if response.status_code == 302 and password:
        assert Project.objects.get(pk=project_id).snapshots.count() == 1

    # since tests use transactions, we cannot test the cleanup here

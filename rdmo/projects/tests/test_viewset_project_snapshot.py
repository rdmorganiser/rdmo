from pathlib import Path

import pytest
from django.conf import settings
from django.urls import reverse

from rdmo.core.constants import VALUE_TYPE_FILE

from ..models import Project, Snapshot

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
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 404
    },
    'detail': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 404
    },
    'create': {
        'owner': 201, 'manager': 201, 'author': 403, 'guest': 403, 'api': 201, 'user': 404, 'site': 201, 'anonymous': 404
    },
    'update': {
        'owner': 200, 'manager': 200, 'author': 403, 'guest': 403, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 404
    },
    'delete': {
        'owner': 405, 'manager': 405, 'author': 405, 'guest': 405, 'api': 405, 'user': 404, 'site': 405, 'anonymous': 404
    }
}

urlnames = {
    'list': 'v1-projects:project-snapshot-list',
    'detail': 'v1-projects:project-snapshot-detail'
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
        for snapshot in response.json():
            assert snapshot['id'] in Snapshot.objects.filter(project_id=project_id).values_list('id', flat=True)


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Snapshot.objects.filter(project_id=project_id)

    for instance in instances:
        url = reverse(urlnames['detail'], args=[project_id, instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()

        if response == 200:
            snapshot = response.json()
            assert snapshot['id'] in Snapshot.objects.filter(project_id=project_id).values_list('id', flat=True)


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, files, username, password):
    client.login(username=username, password=password)

    project = Project.objects.get(pk=project_id)
    snapshot_count = project.snapshots.count()
    values_count = project.values.count()
    current_values_count = project.values.filter(snapshot=None).count()

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'title': 'A new snapshot',
        'description': 'Some description'
    }
    response = client.post(url, data)
    assert response.status_code == status_map['create'][username], response.json()

    if response.status_code == 201:
        assert response.json().get('id') in project.snapshots.values_list('id', flat=True)
        assert project.snapshots.count() == snapshot_count + 1
        assert project.values.count() == values_count + current_values_count

        for file_value in project.values.filter(value_type=VALUE_TYPE_FILE):
            assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()
    else:
        assert project.snapshots.count() == snapshot_count
        assert project.values.count() == values_count


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)

    project = Project.objects.get(pk=project_id)
    snapshots = project.snapshots.all()
    snapshot_count = project.snapshots.count()
    values_count = project.values.count()
    values_files = [value.file.name for value in project.values.filter(value_type=VALUE_TYPE_FILE)]

    for snapshot in snapshots:
        url = reverse(urlnames['detail'], args=[project_id, snapshot.pk])
        data = {
            'title': snapshot.title,
            'description': snapshot.description
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()

        if response == 200:
            assert response.json().get('id') in project.snapshots.values_list('id', flat=True)

        assert project.snapshots.count() == snapshot_count
        assert project.values.count() == values_count
        for file_value in values_files:
            assert Path(settings.MEDIA_ROOT).joinpath(file_value).exists()


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Snapshot.objects.filter(project_id=project_id)

    for instance in instances:
        url = reverse(urlnames['detail'], args=[project_id, instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()

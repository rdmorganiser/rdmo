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

view_snapshot_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'guest': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

add_snapshot_permission_map = change_snapshot_permission_map = delete_snapshot_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

urlnames = {
    'list': 'v1-projects:project-snapshot-list',
    'detail': 'v1-projects:project-snapshot-detail'
}

projects = [1, 2, 3, 4, 5]
snapshots = [1, 3, 7, 4, 5, 6]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_list(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    response = client.get(url)

    if project_id in view_snapshot_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        if username == 'user':
            assert sorted([item['id'] for item in response.json()]) == []
        else:
            values_list = Snapshot.objects.filter(project_id=project_id) \
                                          .order_by('id').values_list('id', flat=True)
            assert sorted([item['id'] for item in response.json()]) == list(values_list)

    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('snapshot_id', snapshots)
def test_detail(db, client, username, password, project_id, snapshot_id):
    client.login(username=username, password=password)
    snapshot = Snapshot.objects.filter(project_id=project_id, id=snapshot_id).filter()

    url = reverse(urlnames['detail'], args=[project_id, snapshot_id])
    response = client.get(url)

    if snapshot and project_id in view_snapshot_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') == snapshot_id
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_create(db, client, files, username, password, project_id):
    client.login(username=username, password=password)
    project = Project.objects.get(id=project_id)

    snapshot_count = project.snapshots.count()
    values_count = project.values.count()
    current_values_count = project.values.filter(snapshot=None).count()

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'title': 'A new snapshot',
        'description': 'Some description'
    }
    response = client.post(url, data)

    if project_id in add_snapshot_permission_map.get(username, []):
        assert response.status_code == 201
        assert isinstance(response.json(), dict)
        assert response.json().get('id') in project.snapshots.values_list('id', flat=True)
        assert project.snapshots.count() == snapshot_count + 1
        assert project.values.count() == values_count + current_values_count

        for file_value in project.values.filter(value_type=VALUE_TYPE_FILE):
            assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()
    else:
        if project_id in view_snapshot_permission_map.get(username, []):
            assert response.status_code == 403
        else:
            assert response.status_code == 404

        assert project.snapshots.count() == snapshot_count
        assert project.values.count() == values_count


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('snapshot_id', snapshots)
def test_update(db, client, username, password, project_id, snapshot_id):
    client.login(username=username, password=password)
    project = Project.objects.get(id=project_id)
    snapshot = Snapshot.objects.filter(project_id=project_id, id=snapshot_id).first()

    snapshot_count = project.snapshots.count()
    values_count = project.values.count()
    values_files = [value.file.name for value in project.values.filter(value_type=VALUE_TYPE_FILE)]

    url = reverse(urlnames['detail'], args=[project_id, snapshot_id])
    data = {
        'title': 'A new title',
        'description': 'A new description'
    }
    response = client.put(url, data, content_type='application/json')

    if snapshot and project_id in change_snapshot_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') in project.snapshots.values_list('id', flat=True)
    elif snapshot and project_id in view_snapshot_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404

    assert project.snapshots.count() == snapshot_count
    assert project.values.count() == values_count
    for file_value in values_files:
        assert Path(settings.MEDIA_ROOT).joinpath(file_value).exists()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('snapshot_id', snapshots)
def test_delete(db, client, username, password, project_id, snapshot_id):
    client.login(username=username, password=password)
    project = Project.objects.get(id=project_id)

    snapshot_count = project.snapshots.count()
    values_count = project.values.count()
    values_files = [value.file.name for value in project.values.filter(value_type=VALUE_TYPE_FILE)]

    url = reverse(urlnames['detail'], args=[project_id, snapshot_id])
    response = client.delete(url)

    if project_id in view_snapshot_permission_map.get(username, []):
        assert response.status_code == 405
    else:
        assert response.status_code == 404

    assert project.snapshots.count() == snapshot_count
    assert project.values.count() == values_count
    for file_value in values_files:
        assert Path(settings.MEDIA_ROOT).joinpath(file_value).exists()

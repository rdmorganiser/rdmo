from pathlib import Path

import pytest
from django.conf import settings
from django.urls import reverse

from rdmo.core.constants import VALUE_TYPE_FILE

from ..models import Project, Snapshot, Value

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
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

add_snapshot_permission_map = change_snapshot_permission_map = rollback_snapshot_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

projects = [1, 2, 3, 4, 5]
snapshots = [1, 3, 7, 4, 5, 6]

snapshots_project = 1


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_snapshot_create_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('snapshot_create', args=[project_id])
    response = client.get(url)

    if project_id in add_snapshot_permission_map.get(username, []):
        assert response.status_code == 200
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_snapshot_create_post(db, client, files, username, password, project_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)

    snapshot_count = project.snapshots.count()
    values_count = project.values.count()
    current_values_count = project.values.filter(snapshot=None).count()

    url = reverse('snapshot_create', args=[project.id])
    data = {
        'title': 'A new snapshot',
        'description': 'Some description'
    }
    response = client.post(url, data)

    # check if all the files are where are supposed to be
    for file_value in Value.objects.filter(value_type=VALUE_TYPE_FILE):
        assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()

    if project.id in add_snapshot_permission_map.get(username, []):
        assert response.status_code == 302
        assert project.snapshots.count() == snapshot_count + 1
        assert project.values.count() == values_count + current_values_count
        for file_value in project.values.filter(value_type=VALUE_TYPE_FILE):
            assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302

        assert project.snapshots.count() == snapshot_count
        assert project.values.count() == values_count


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('snapshot_id', snapshots)
def test_snapshot_update_get(db, client, username, password, project_id, snapshot_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)

    url = reverse('snapshot_update', args=[project_id, snapshot_id])
    response = client.get(url)

    # check if all the files are where are supposed to be
    for file_value in Value.objects.filter(value_type=VALUE_TYPE_FILE):
        assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()

    if snapshot_id in project.snapshots.values_list('id', flat=True):
        if project_id in change_snapshot_permission_map.get(username, []):
            assert response.status_code == 200
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('snapshot_id', snapshots)
def test_snapshot_update_post(db, client, username, password, project_id, snapshot_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)
    snapshot = Snapshot.objects.get(pk=snapshot_id)

    snapshot_count = project.snapshots.count()
    values_count = project.values.count()
    values_files = [value.file.name for value in project.values.filter(value_type=VALUE_TYPE_FILE)]

    url = reverse('snapshot_update', args=[project_id, snapshot_id])
    data = {
        'title': snapshot.title,
        'description': snapshot.description
    }
    response = client.post(url, data)

    # check if all the files are where are supposed to be
    for file_value in Value.objects.filter(value_type=VALUE_TYPE_FILE):
        assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()

    if snapshot_id in Project.objects.get(pk=project_id).snapshots.values_list('id', flat=True):
        if project_id in change_snapshot_permission_map.get(username, []):
            assert response.status_code == 302
            for file_value in project.values.filter(value_type=VALUE_TYPE_FILE):
                assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
    else:
        assert response.status_code == 404

    assert Project.objects.get(pk=project_id).snapshots.count() == snapshot_count
    assert Project.objects.get(pk=project_id).values.count() == values_count
    for file_value in values_files:
        assert Path(settings.MEDIA_ROOT).joinpath(file_value).exists()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('snapshot_id', snapshots)
def test_snapshot_rollback_get(db, client, username, password, project_id, snapshot_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)
    project_snapshots = list(project.snapshots.values_list('id', flat=True))

    url = reverse('snapshot_rollback', args=[project_id, snapshot_id])
    response = client.get(url)

    if snapshot_id in project_snapshots:
        if project_id in rollback_snapshot_permission_map.get(username, []):
            assert response.status_code == 200
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('snapshot_id', snapshots)
def test_snapshot_rollback_post(db, client, files, username, password, project_id, snapshot_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)
    project_snapshots = list(project.snapshots.values_list('id', flat=True))

    url = reverse('snapshot_rollback', args=[project_id, snapshot_id])
    response = client.post(url)

    # check if all the files are where are supposed to be
    for file_value in Value.objects.filter(value_type=VALUE_TYPE_FILE):
        assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()

    if snapshot_id in project_snapshots:
        if project_id in rollback_snapshot_permission_map.get(username, []):
            assert response.status_code == 302
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
    else:
        assert response.status_code == 404

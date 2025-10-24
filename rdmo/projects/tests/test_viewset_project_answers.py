import pytest

from django.urls import reverse

from ..models import Snapshot

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('admin', 'admin'),
    ('api', 'api'),
    ('site', 'site'),
    ('user', 'user'),
    ('anonymous', None),
)

view_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10, 12],
    'manager': [1, 3, 5, 7, 12],
    'author': [1, 3, 5, 8, 12],
    'guest': [1, 3, 5, 9, 12],
    'admin': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'user': [12]
}

projects = [1, 2, 3, 4, 5, 12]

snapshots = [1, 3]

export_formats = ['html']

urlnames = {
    'answers': 'v1-projects:project-answers',
    'answers-snapshot': 'v1-projects:project-answers-snapshot',
    'answers-export': 'v1-projects:project-answers-export',
    'answers-export-snapshot': 'v1-projects:project-answers-export-snapshot',
}

@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_view(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['answers'], args=[project_id])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('snapshot_id', snapshots)
def test_view_snapshot(db, client, username, password, snapshot_id):
    client.login(username=username, password=password)
    snapshot = Snapshot.objects.get(pk=snapshot_id)

    url = reverse(urlnames['answers-snapshot'], args=[snapshot.project.id, snapshot_id])
    response = client.get(url)

    if snapshot.project.id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('export_format', export_formats)
def test_view_export(db, client, username, password, project_id, export_format):
    client.login(username=username, password=password)

    url = reverse(urlnames['answers-export'], args=[project_id, export_format])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('snapshot_id', snapshots)
@pytest.mark.parametrize('export_format', export_formats)
def test_view_snapshot_export(db, client, username, password, snapshot_id, export_format):
    client.login(username=username, password=password)
    snapshot = Snapshot.objects.get(pk=snapshot_id)

    url = reverse(urlnames['answers-export-snapshot'], args=[snapshot.project.id, snapshot_id, export_format])
    response = client.get(url)

    if snapshot.project.id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401

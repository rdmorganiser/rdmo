import pytest

from django.urls import reverse

from ..models import Project, Snapshot

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

views = (1, 2)

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
    'views': 'v1-projects:project-views',
    'view': 'v1-projects:project-view',
    'view-snapshot': 'v1-projects:project-view-snapshot',
    'view-export': 'v1-projects:project-view-export',
    'view-export-snapshot': 'v1-projects:project-view-export-snapshot',
}


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_views(db, client, username, password, project_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)
    project_views = list(project.views.values_list('id', flat=True))

    url = reverse(urlnames['views'], args=[project_id])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert [item['id'] for item in response.json()] == project_views
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('view_id', views)
def test_view(db, client, username, password, project_id, view_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)
    project_views = list(project.views.values_list('id', flat=True))

    url = reverse(urlnames['view'], args=[project_id, view_id])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []) and view_id in project_views:
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('snapshot_id', snapshots)
@pytest.mark.parametrize('view_id', views)
def test_view_snapshot(db, client, username, password, snapshot_id, view_id):
    client.login(username=username, password=password)
    snapshot = Snapshot.objects.get(pk=snapshot_id)
    project_views = list(snapshot.project.views.values_list('id', flat=True))

    url = reverse(urlnames['view-snapshot'], args=[snapshot.project.id, snapshot_id, view_id])
    response = client.get(url)

    if snapshot.project.id in view_project_permission_map.get(username, []) and view_id in project_views:
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
def test_view_snapshot_snapshot_not_found(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['view-snapshot'], args=[1, 100, 1])
    response = client.get(url)

    if password:
        assert response.status_code == 404
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
def test_view_snapshot_view_not_found(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['view-snapshot'], args=[1, 1, 100])
    response = client.get(url)

    if password:
        assert response.status_code == 404
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('view_id', views)
@pytest.mark.parametrize('export_format', export_formats)
def test_view_export(db, client, username, password, project_id, view_id, export_format):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)
    project_views = list(project.views.values_list('id', flat=True))

    url = reverse(urlnames['view-export'], args=[project_id, view_id, export_format])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []) and view_id in project_views:
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('snapshot_id', snapshots)
@pytest.mark.parametrize('view_id', views)
@pytest.mark.parametrize('export_format', export_formats)
def test_view_snapshot_export(db, client, username, password, snapshot_id, view_id, export_format):
    client.login(username=username, password=password)
    snapshot = Snapshot.objects.get(pk=snapshot_id)
    project_views = list(snapshot.project.views.values_list('id', flat=True))

    url = reverse(urlnames['view-export-snapshot'], args=[snapshot.project.id, snapshot_id, view_id, export_format])
    response = client.get(url)

    if snapshot.project.id in view_project_permission_map.get(username, []) and view_id in project_views:
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
def test_view_snapshot_export_snapshot_not_found(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['view-export-snapshot'], args=[1, 100, 1, 'html'])
    response = client.get(url)

    if password:
        assert response.status_code == 404
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
def test_view_snapshot_export_view_not_found(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['view-export-snapshot'], args=[1, 1, 100, 'html'])
    response = client.get(url)

    if password:
        assert response.status_code == 404
    else:
        assert response.status_code == 401

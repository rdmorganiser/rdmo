import pytest

from django.urls import reverse

from rdmo.questions.models import Catalog

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

urlnames = {
    'answers-tree': 'v1-projects:project-answers',
    'answers-tree-snapshot': 'v1-projects:project-answers-snapshot',
}

@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_view(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['answers-tree'], args=[project_id])
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

    url = reverse(urlnames['answers-tree-snapshot'], args=[snapshot.project.id, snapshot_id])
    response = client.get(url)

    if snapshot.project.id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('snapshot_id', [None, 1])
def test_view_without_catalog(db, client, snapshot_id):
    project = Project.objects.get(pk=1)
    project.catalog.delete()
    project.refresh_from_db()

    client.login(username='owner', password='owner')
    urlname = (
        'v1-projects:project-answers-tree-snapshot' if snapshot_id is not None else 'v1-projects:project-answers-tree'
    )
    args = [project.pk, snapshot_id] if snapshot_id is not None else [project.pk]
    response = client.get(reverse(urlname, args=args))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] is None
    assert data['show'] is False
    assert data['elements'] == []
    assert data['count'] == data['total'] == 0


def test_view_empty_catalog(db, client):
    project = Project.objects.get(pk=1)
    catalog = Catalog.objects.create(uri_path='empty', title_lang1='Empty catalog')
    project.catalog = catalog
    project.save()
    client.login(username='owner', password='owner')
    response = client.get(reverse('v1-projects:project-answers-tree', args=[project.pk]))
    assert response.status_code == 200
    assert response.json()['id'] == catalog.pk
    assert response.json()['show'] is True
    assert response.json()['elements'] == []


@pytest.mark.parametrize('username,password', users)
def test_view_snapshot_not_found(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['answers-tree-snapshot'], args=[1, 100])
    response = client.get(url)

    if password:
        assert response.status_code == 404
    else:
        assert response.status_code == 401


def test_view_snapshot_not_found_without_catalog(db, client):
    project = Project.objects.get(pk=1)
    project.catalog.delete()
    project.refresh_from_db()

    client.login(username='owner', password='owner')
    response = client.get(reverse('v1-projects:project-answers-tree-snapshot', args=[project.pk, 999999]))
    assert response.status_code == 404

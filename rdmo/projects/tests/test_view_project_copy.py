import pytest

from django.contrib.auth.models import Group, User
from django.urls import reverse

from ..models import Project, Snapshot, Value

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('api', 'api'),
)

view_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10],
    'manager': [1, 3, 5, 7],
    'author': [1, 3, 5, 8],
    'guest': [1, 3, 5, 9],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
}

change_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10],
    'manager': [1, 3, 5, 7],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
}

delete_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
}

export_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10],
    'manager': [1, 3, 5, 7],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
}

projects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

project_id = 1
site_id = 1
parent_id = 1
catalog_id = 1


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_copy_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_copy', args=[project_id])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


def test_project_copy_restricted_get(db, client, settings):
    settings.PROJECT_CREATE_RESTRICTED = True
    settings.PROJECT_CREATE_GROUPS = ['projects']

    group = Group.objects.create(name='projects')
    guest = User.objects.get(username='guest')
    guest.groups.add(group)

    client.login(username='guest', password='guest')

    url = reverse('project_copy', args=[project_id])
    response = client.get(url)

    assert response.status_code == 200


def test_project_copy_forbidden_get(db, client, settings):
    settings.PROJECT_CREATE_RESTRICTED = True

    client.login(username='guest', password='guest')

    url = reverse('project_copy', args=[project_id])
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_copy_post(db, files, client, username, password, project_id):
    client.login(username=username, password=password)

    project_count = Project.objects.count()
    snapshot_count = Snapshot.objects.count()
    value_count = Value.objects.count()

    project = Project.objects.get(id=project_id)
    project_snapshots_count = project.snapshots.count()
    project_values_count = project.values.count()

    url = reverse('project_copy', args=[project_id])
    data = {
        'title': 'A new project',
        'description': 'Some description',
        'catalog': catalog_id
    }
    response = client.post(url, data)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 302
        assert Project.objects.count() == project_count + 1
        assert Snapshot.objects.count() == snapshot_count + project_snapshots_count
        assert Value.objects.count() == value_count + project_values_count
    else:
        assert response.status_code == 403 if password else 302
        assert Project.objects.count() == project_count
        assert Value.objects.count() == value_count


def test_project_copy_post_restricted(db, files, client, settings):
    settings.PROJECT_CREATE_RESTRICTED = True
    settings.PROJECT_CREATE_GROUPS = ['projects']

    group = Group.objects.create(name='projects')
    guest = User.objects.get(username='guest')
    guest.groups.add(group)

    client.login(username='guest', password='guest')

    url = reverse('project_copy', args=[project_id])
    data = {
        'title': 'A new project',
        'description': 'Some description',
        'catalog': catalog_id
    }
    response = client.post(url, data)

    assert response.status_code == 302


def test_project_copy_post_forbidden(db, files, client, settings):
    settings.PROJECT_CREATE_RESTRICTED = True

    client.login(username='guest', password='guest')

    url = reverse('project_copy', args=[project_id])
    data = {
        'title': 'A new project',
        'description': 'Some description',
        'catalog': catalog_id
    }
    response = client.post(url, data)

    assert response.status_code == 403


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_copy_parent_post(db, files, client, username, password, project_id):
    client.login(username=username, password=password)
    project_count = Project.objects.count()

    project_count = Project.objects.count()
    snapshot_count = Snapshot.objects.count()
    value_count = Value.objects.count()

    project = Project.objects.get(id=project_id)
    project_snapshots_count = project.snapshots.count()
    project_values_count = project.values.count()

    url = reverse('project_copy', args=[project_id])
    data = {
        'title': 'A new project',
        'description': 'Some description',
        'catalog': catalog_id,
        'parent': parent_id
    }
    response = client.post(url, data)

    if project_id in view_project_permission_map.get(username, []):
        if parent_id in view_project_permission_map.get(username, []):
            assert response.status_code == 302
            assert Project.objects.count() == project_count + 1
            assert Snapshot.objects.count() == snapshot_count + project_snapshots_count
            assert Value.objects.count() == value_count + project_values_count
        else:
            assert response.status_code == 200
            assert Project.objects.count() == project_count
            assert Value.objects.count() == value_count
    else:
        assert response.status_code == 403 if password else 302
        assert Project.objects.count() == project_count
        assert Value.objects.count() == value_count

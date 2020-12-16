import os
import re
from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

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

change_project_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

projects = [1, 2, 3, 4, 5]


@pytest.mark.parametrize('username,password', users)
def test_project_create_upload_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_upload')
    response = client.get(url)
    if password:
        assert response.status_code == 302
        assert response.url == '/projects/'
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
def test_project_create_upload_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_upload')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if password:
        assert response.status_code == 200
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
def test_project_create_upload_post_error(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_upload')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'error.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if password:
        assert response.status_code == 400
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
def test_project_create_upload_post_empty(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_upload')
    response = client.post(url)
    if password:
        assert response.status_code == 302
        assert response.url == '/projects/'
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_import')
    response = client.get(url)
    if password:
        assert response.status_code == 302
        assert response.url == '/projects/'
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post(db, settings, client, files, username, password):
    client.login(username=username, password=password)
    projects_count = Project.objects.count()

    # upload file
    url = reverse('project_create_upload')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if password:
        assert response.status_code == 200

        # get keys from the response
        keys = re.findall(r'name=\"(.*?)\"', response.content.decode())

        # import file
        url = reverse('project_create_import')
        data = {key: ['on'] for key in keys}
        response = client.post(url, data)

        # assert that the project exists and that there are values
        if password:
            project = Project.objects.order_by('updated').last()
            assert response.status_code == 302
            assert response.url == '/projects/{}/'.format(project.pk)

            # a new project, new values values
            assert Project.objects.count() == projects_count + 1
            assert project.values.count() > 0
        else:
            assert response.status_code == 302
            assert response.url.startswith('/account/login/')

            # no new project was created
            assert Project.objects.count() == projects_count
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post_error(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_import')
    response = client.post(url)
    if password:
        assert response.status_code == 400
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post_empty(db, settings, client, username, password):
    client.login(username=username, password=password)
    projects_count = Project.objects.count()

    # upload file
    url = reverse('project_create_upload')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if password:
        assert response.status_code == 200

        url = reverse('project_create_import')
        response = client.post(url)

        # assert that the project exists, but that there are not values
        if password:
            new_project = Project.objects.order_by('updated').last()
            assert response.status_code == 302
            assert response.url == '/projects/{}/'.format(new_project.id)

            # a new project, but no values
            assert Project.objects.count() == projects_count + 1
            assert new_project.values.count() == 0
        else:
            assert response.status_code == 302
            assert response.url.startswith('/account/login/')

            # no new project was created
            assert Project.objects.count() == projects_count
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_upload_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_upload', args=[project_id])
    response = client.get(url)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 302
        assert response.url == '/projects/{}/'.format(project_id)
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_upload_post(db, settings, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_upload', args=[project_id])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

        if project_id in change_project_permission_map.get(username, []):
            assert response.status_code == 200
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
            assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_upload_post_error(db, settings, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_upload', args=[project_id])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'error.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 400
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_upload_post_empty(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_upload', args=[project_id])
    response = client.post(url)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 302
        assert response.url == '/projects/{}/'.format(project_id)
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_import_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_import', args=[project_id])
    response = client.get(url)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 302
        assert response.url == '/projects/{}/'.format(project_id)
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_import_post(db, settings, client, files, username, password, project_id):
    client.login(username=username, password=password)
    projects_count = Project.objects.count()
    project = Project.objects.get(pk=project_id)
    project_snapshot_count = project.snapshots.count()
    project_values_count = project.values.count()
    snapshot_values_count = project.values.filter(snapshot=None).count()

    # upload file
    url = reverse('project_update_upload', args=[project_id])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 200

        # get keys from the response
        keys = re.findall(r'name=\"(.*?)\"', response.content.decode())

        # import file
        url = reverse('project_update_import', args=[project_id])
        data = {key: ['on'] for key in keys}
        response = client.post(url, data)

        # no new project, snapshots, values were created
        project = Project.objects.get(pk=project_id)

        assert Project.objects.count() == projects_count
        assert project.snapshots.count() == project_snapshot_count
        if project_values_count > 0:
            assert project.values.count() == project_values_count
        if snapshot_values_count > 0:
            assert project.values.filter(snapshot=None).count() == snapshot_values_count
        assert timezone.now() - project.updated > timedelta(days=1)

        for snapshot in project.snapshots.all():
            assert timezone.now() - snapshot.updated > timedelta(days=1)
            for value in snapshot.values.all():
                assert timezone.now() - value.updated > timedelta(days=1)

        if project_id in change_project_permission_map.get(username, []):
            assert response.status_code == 302
            assert response.url == '/projects/{}/'.format(project_id)

            for value in project.values.filter(snapshot=None):
                assert timezone.now() - value.updated < timedelta(days=1), value
        else:
            if password:
                assert response.status_code == 403
            else:
                assert response.status_code == 302
                assert response.url.startswith('/account/login/')

            for value in project.values.filter(snapshot=None):
                assert timezone.now() - value.updated > timedelta(days=1), value

    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_import_post_error(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_import', args=[project_id])
    response = client.post(url)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 400
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_import_empty(db, settings, client, username, password, project_id):
    client.login(username=username, password=password)
    projects_count = Project.objects.count()
    project = Project.objects.get(pk=project_id)
    project_snapshot_count = project.snapshots.count()
    project_values_count = project.values.count()
    snapshot_values_count = project.values.filter(snapshot=None).count()

    # upload file
    url = reverse('project_update_upload', args=[project_id])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 200, project_id

        response = client.post(url)

        # no new project, snapshots, values were created
        project = Project.objects.get(pk=project_id)
        assert Project.objects.count() == projects_count
        assert project.snapshots.count() == project_snapshot_count
        assert project.values.count() == project_values_count
        assert project.values.filter(snapshot=None).count() == snapshot_values_count
        assert timezone.now() - project.updated > timedelta(days=1)
        for value in project.values.filter(snapshot=None):
            assert timezone.now() - value.updated > timedelta(days=1)
        for snapshot in project.snapshots.all():
            assert timezone.now() - snapshot.updated > timedelta(days=1)
            for value in snapshot.values.all():
                assert timezone.now() - value.updated > timedelta(days=1)

        assert response.status_code == 302
        assert response.url == '/projects/{}/'.format(project_id)
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')

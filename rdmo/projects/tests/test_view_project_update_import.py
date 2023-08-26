import os
import re
from pathlib import Path

import pytest

from django.urls import reverse

from rdmo.core.constants import VALUE_TYPE_FILE

from ..models import Project, Value

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

view_project_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'guest': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

change_project_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

projects = [1, 2, 3, 4, 5]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_import_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_import', args=[project_id])
    response = client.get(url)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 400
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_import_post_error(db, settings, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_import', args=[project_id])
    response = client.post(url, {
        'method': 'wrong'
    })

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 404
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_import_post_upload_file(db, settings, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_import', args=[project_id])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {
            'method': 'upload_file',
            'uploaded_file': f
        })

        if project_id in change_project_permission_map.get(username, []):
            assert response.status_code == 302
            assert response.url.startswith(f'/projects/{project_id}/import/')

            # follow the redirect to the import form
            response = client.get(response.url)
            assert response.status_code == 200
            assert b'Import from project.xml' in response.content
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
            assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_import_post_upload_file_error(db, settings, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_import', args=[project_id])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'error.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {
            'method': 'upload_file',
            'uploaded_file': f
        })

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 302
        assert response.url.startswith(f'/projects/{project_id}/import/')

        # follow the redirect to the import form
        response = client.get(response.url)
        assert response.status_code == 400
        assert b'Files of this type cannot be imported.' in response.content
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_import_post_upload_file_empty(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_import', args=[project_id])
    response = client.post(url, {
        'method': 'upload_file'
    })

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 400
        assert b'There has been an error with your import.' in response.content
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_import_post_import_file(db, settings, client, files, username, password, project_id):
    client.login(username=username, password=password)
    projects_count = Project.objects.count()

    project = Project.objects.get(pk=project_id)
    project_updated = project.updated
    project_snapshot_count = project.snapshots.count()
    project_snapshot_values_count = project.values.filter(snapshot=None).count()
    project_values_count = project.values.count()

    # upload file
    url = reverse('project_update_import', args=[project_id])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url,  {
            'method': 'upload_file',
            'uploaded_file': f
        })

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 302
        assert response.url.startswith(f'/projects/{project_id}/import/')

        # follow the redirect to the import form
        response = client.get(response.url)

        assert response.status_code == 200

        # get keys from the response
        keys = re.findall(r'name=\"(http.*?)\"', response.content.decode())

        # import file
        url = reverse('project_update_import', args=[project_id])
        data = {key: ['on'] for key in keys}
        data.update({'method': 'import_file'})
        response = client.post(url, data)

        # check if all the files are where are supposed to be
        for file_value in Value.objects.filter(value_type=VALUE_TYPE_FILE):
            assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()

        # no new project, snapshots, values were created
        project = Project.objects.get(pk=project_id)

        assert Project.objects.count() == projects_count
        assert project.snapshots.count() == project_snapshot_count
        if project_id == 1:
            assert project.values.count() == project_values_count
            assert project.values.filter(snapshot=None).count() == project_snapshot_values_count

        assert project.updated == project_updated

        if project_id in change_project_permission_map.get(username, []):
            assert response.status_code == 302
            assert response.url == f'/projects/{project_id}/'

        else:
            if password:
                assert response.status_code == 403
            else:
                assert response.status_code == 302
                assert response.url.startswith('/account/login/')

    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_import_post_import_file_cancel(db, settings, client, files, username, password, project_id):
    client.login(username=username, password=password)
    projects_count = Project.objects.count()

    project = Project.objects.get(pk=project_id)
    project_updated = project.updated
    project_snapshot_count = project.snapshots.count()
    project_snapshot_values_count = project.values.filter(snapshot=None).count()
    project_values_count = project.values.count()

    # upload file
    url = reverse('project_update_import', args=[project_id])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url,  {
            'method': 'upload_file',
            'uploaded_file': f
        })

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 302
        assert response.url.startswith(f'/projects/{project_id}/import/')

        # follow the redirect to the import form
        response = client.get(response.url)

        assert response.status_code == 200

        # get keys from the response
        keys = re.findall(r'name=\"(http.*?)\"', response.content.decode())

        # import file
        url = reverse('project_update_import', args=[project_id])
        data = {key: ['on'] for key in keys}
        data.update({'method': 'import_file', 'cancel': 'Cancel'})
        response = client.post(url, data)

        # check if all the files are where are supposed to be
        for file_value in Value.objects.filter(value_type=VALUE_TYPE_FILE):
            assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()

        # no new project, snapshots, values were created
        project = Project.objects.get(pk=project_id)
        assert Project.objects.count() == projects_count
        assert project.snapshots.count() == project_snapshot_count
        assert project.values.count() == project_values_count
        assert project.values.filter(snapshot=None).count() == project_snapshot_values_count
        assert project.updated == project_updated

        assert response.status_code == 302
        assert response.url == f'/projects/{project_id}/'
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_import_post_import_file_empty(db, settings, client, username, password, project_id):
    client.login(username=username, password=password)
    projects_count = Project.objects.count()

    project = Project.objects.get(pk=project_id)
    project_updated = project.updated
    project_snapshot_count = project.snapshots.count()
    project_snapshot_values_count = project.values.filter(snapshot=None).count()
    project_values_count = project.values.count()

    # upload file
    url = reverse('project_update_import', args=[project_id])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {
            'method': 'upload_file',
            'uploaded_file': f
        })

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 302
        assert response.url.startswith(f'/projects/{project_id}/import/')

        # follow the redirect to the import form, this will set import_key in the session
        response = client.get(response.url)

        assert response.status_code == 200

        # post the form empty
        response = client.post(url, {
            'method': 'import_file'
        })

        # check if all the files are where are supposed to be
        for file_value in Value.objects.filter(value_type=VALUE_TYPE_FILE):
            assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()

        # no new project, snapshots, values were created
        project = Project.objects.get(pk=project_id)
        assert Project.objects.count() == projects_count
        assert project.snapshots.count() == project_snapshot_count
        assert project.values.count() == project_values_count
        assert project.values.filter(snapshot=None).count() == project_snapshot_values_count
        assert project.updated == project_updated

        assert response.status_code == 302
        assert response.url == f'/projects/{project_id}/'
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('source_id', projects)
def test_project_update_import_post_import_project_step1(db, settings, client, username, password,
                                                         project_id, source_id):
    client.login(username=username, password=password)

    url = reverse('project_update_import', args=[project_id])
    response = client.post(url, {
        'method': 'import_project',
        'source': source_id
    })

    if project_id in change_project_permission_map.get(username, []):
        if source_id in view_project_permission_map.get(username, []):
            assert response.status_code == 200
        else:
            assert response.status_code == 403

    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('source_id', projects)
def test_project_update_import_post_import_project_step2(db, settings, client, username, password,
                                                         project_id, source_id):
    client.login(username=username, password=password)
    projects_count = Project.objects.count()

    project = Project.objects.get(pk=project_id)
    project_updated = project.updated
    project_snapshot_count = project.snapshots.count()
    project_snapshot_values_count = project.values.filter(snapshot=None).count()
    project_values_count = project.values.count()

    source = Project.objects.get(pk=source_id)
    source_snapshot_count = source.snapshots.count()
    source_snapshot_values_count = source.values.filter(snapshot=None).count()
    source_values_count = source.values.count()

    url = reverse('project_update_import', args=[project_id])
    response = client.post(url, {
        'method': 'import_project',
        'source': source_id
    })

    if project_id in change_project_permission_map.get(username, []):
        if source_id in view_project_permission_map.get(username, []):
            assert response.status_code == 200

            # get keys from the response
            keys = re.findall(r'name=\"(http.*?)\"', response.content.decode())

            # import file
            url = reverse('project_update_import', args=[project_id])
            data = {key: ['on'] for key in keys}
            data.update({
                'method': 'import_project',
                'source': source_id
            })
            response = client.post(url, data)

            # check if all the files are where are supposed to be
            for file_value in Value.objects.filter(value_type=VALUE_TYPE_FILE):
                assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()

            # no new project, snapshots, values were created
            project = Project.objects.get(pk=project_id)
            source = Project.objects.get(pk=source_id)

            # no new project was created
            assert Project.objects.count() == projects_count

            # the project has the correct count of snapshot and values
            assert project.snapshots.count() == project_snapshot_count
            if project_id == 1:
                assert project.values.count() == project_values_count
                assert project.values.filter(snapshot=None).count() == project_snapshot_values_count

            # the source project has the correct count of snapshot and values
            assert source.snapshots.count() == source_snapshot_count
            if source_id == 1:
                assert source.values.count() == source_values_count
                assert source.values.filter(snapshot=None).count() == source_snapshot_values_count

            assert project.updated == project_updated

            if project_id in change_project_permission_map.get(username, []):
                assert response.status_code == 302
                assert response.url == f'/projects/{project_id}/'

            else:
                if password:
                    assert response.status_code == 403
                else:
                    assert response.status_code == 302
                    assert response.url.startswith('/account/login/')
        else:
            assert response.status_code == 403

    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_import_post_import_project_error(db, settings, client, username, password, project_id):
    client.login(username=username, password=password)

    # upload file
    url = reverse('project_update_import', args=[project_id])
    response = client.post(url, {
        'method': 'import_project'
    })

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 404
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')

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

change_project_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

projects = [1, 2, 3, 4, 5]


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_import')
    response = client.get(url)
    if password:
        assert response.status_code == 400
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post_empty(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_import')
    response = client.post(url)

    if password:
        assert response.status_code == 404
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post_upload_file(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_import')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {
            'method': 'upload_file',
            'uploaded_file': f
        })

    if password:
        assert response.status_code == 302
        assert response.url.startswith('/projects/import/')

        # follow the redirect to the import form
        response = client.get(response.url)
        assert response.status_code == 200
        assert b'Create project from project.xml' in response.content
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post_upload_file_error(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_import')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'error.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {
            'method': 'upload_file',
            'uploaded_file': f
        })

    if password:
        assert response.status_code == 302
        assert response.url.startswith('/projects/import/')

        # follow the redirect to the import form
        response = client.get(response.url)
        assert response.status_code == 400
        assert b'Files of this type cannot be imported.' in response.content
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post_upload_file_empty(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_import')
    response = client.post(url, {
        'method': 'upload_file'
    })
    if password:
        assert response.status_code == 400
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post_import_file(db, settings, client, files, username, password):
    client.login(username=username, password=password)
    projects_count = Project.objects.count()

    # upload file
    url = reverse('project_create_import')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {
            'method': 'upload_file',
            'uploaded_file': f
        })

    if password:
        assert response.status_code == 302
        assert response.url.startswith('/projects/import/')

        # follow the redirect to the import form
        response = client.get(response.url)

        assert response.status_code == 200

        # get keys from the response
        keys = re.findall(r'name=\"(http.*?)\"', response.content.decode())

        # import file
        data = {key: ['on'] for key in keys}
        data.update({'method': 'import_file'})
        response = client.post(url, data)

        # check if all the files are where are supposed to be
        for file_value in Value.objects.filter(value_type=VALUE_TYPE_FILE):
            assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()

        # assert that the project exists and that there are values
        if password:
            project = Project.objects.order_by('updated').last()
            assert response.status_code == 302
            assert response.url == f'/projects/{project.pk}/'

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
def test_project_create_import_post_import_file_cancel(db, settings, client, files, username, password):
    client.login(username=username, password=password)
    projects_count = Project.objects.count()

    # upload file
    url = reverse('project_create_import')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {
            'method': 'upload_file',
            'uploaded_file': f
        })

    if password:
        assert response.status_code == 302
        assert response.url.startswith('/projects/import/')

        # follow the redirect to the import form
        response = client.get(response.url)

        assert response.status_code == 200

        # get keys from the response
        keys = re.findall(r'name=\"(http.*?)\"', response.content.decode())

        # import file
        data = {key: ['on'] for key in keys}
        data.update({'method': 'import_file', 'cancel': 'Cancel'})
        response = client.post(url, data)

        # check if all the files are where are supposed to be
        for file_value in Value.objects.filter(value_type=VALUE_TYPE_FILE):
            assert Path(settings.MEDIA_ROOT).joinpath(file_value.file.name).exists()

        # assert that the project exists, but that there are not values
        if password:
            assert response.status_code == 302
            assert response.url == '/projects/'

            # no new project
            assert Project.objects.count() == projects_count
        else:
            assert response.status_code == 302
            assert response.url.startswith('/account/login/')

            # no new project was created
            assert Project.objects.count() == projects_count
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post_import_empty(db, settings, client, username, password):
    client.login(username=username, password=password)
    projects_count = Project.objects.count()

    # upload file
    url = reverse('project_create_import')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {
            'method': 'upload_file',
            'uploaded_file': f
        })

    if password:
        assert response.status_code == 302
        assert response.url.startswith('/projects/import/')

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

        # assert that the project exists, but that there are not values
        if password:
            new_project = Project.objects.order_by('updated').last()
            assert response.status_code == 302
            assert response.url == f'/projects/{new_project.id}/'

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
def test_project_create_import_post_import_project(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_import')
    response = client.post(url, {
        'method': 'import_project'
    })

    if password:
        assert response.status_code == 404
    else:
        assert response.status_code == 302
        assert response.url.startswith('/account/login/')

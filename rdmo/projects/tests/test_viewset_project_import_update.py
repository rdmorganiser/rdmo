import shutil

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

users = (
    'owner',
    'manager',
    'author',
    'guest',
    'admin',
    'api',
    'site',
    'user',
    'anonymous',
)

import_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10, 12],
    'manager': [1, 3, 5, 7],
    'admin': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
}

projects = [1, 2, 3, 4, 5, 12]

plugin_keys = [
    'xml',
    'set',
    'url',
]

plugin_upload = [
    'xml',
]

urlnames = {
    'import': 'v1-projects:project-update-import',
    'upload': 'v1-projects:project-update-upload',
}

xml_file = 'testing/xml/project.xml'


@pytest.mark.parametrize('username', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('plugin_key', plugin_keys)
def test_import_get(db, client, login, username, project_id, plugin_key):
    login(username)

    url = reverse(urlnames['import'], args=[project_id, plugin_key])
    response = client.get(url)

    if username == 'anonymous':
        assert response.status_code == 401
    elif project_id in import_project_permission_map.get(username, []):
        assert response.status_code == (404 if plugin_key in plugin_upload else 200)
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('plugin_key', plugin_keys)
def test_import_post(db, client, login, username, project_id, plugin_key):
    login(username)

    url = reverse(urlnames['import'], args=[project_id, plugin_key])
    response = client.post(url)

    if username == 'anonymous':
        assert response.status_code == 401
    elif project_id in import_project_permission_map.get(username, []):
        assert response.status_code == (404 if plugin_key in plugin_upload else 200)
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username', users)
@pytest.mark.parametrize('project_id', projects)
def test_upload_post(db, client, login, username, project_id):
    login(username)

    url = reverse(urlnames['upload'], args=[project_id])
    with open(xml_file, 'rb') as fp:
        response = client.post(url, {'uploaded_file': fp})

    if username == 'anonymous':
        assert response.status_code == 401
    elif project_id in import_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert response.json().get('key') == 'xml'
        assert client.session.get('rdmo.projects.imports.XMLImport.xml.file_name')
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username', users)
@pytest.mark.parametrize('project_id', projects)
def test_import_post_submit(db, client, login, username, project_id, tmp_path):
    login(username)

    file_name = shutil.copy(xml_file, tmp_path)

    session = client.session
    session['rdmo.projects.imports.XMLImport.xml.file_name'] = str(file_name)
    session.save()

    url = reverse(urlnames['import'], args=[project_id, 'xml'])
    response = client.post(url)

    if username == 'anonymous':
        assert response.status_code == 401
    elif project_id in import_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        assert response.status_code == 404


def test_upload_post_no_file(db, client, login):
    login('owner')

    url = reverse(urlnames['upload'], args=[1])
    response = client.post(url)

    assert response.status_code == 400
    assert 'uploaded_file' in response.json()


def test_upload_post_unknown_file(db, client, login):
    login('owner')

    url = reverse(urlnames['upload'], args=[1])
    response = client.post(url, {'uploaded_file': SimpleUploadedFile('project.txt', b'not a project')})

    assert response.status_code == 400
    assert 'uploaded_file' in response.json()

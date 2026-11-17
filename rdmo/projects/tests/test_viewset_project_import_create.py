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

plugin_keys = [
    'xml',
    'url',
]

plugin_upload = [
    'xml',
]

urlnames = {
    'import': 'v1-projects:project-create-import',
    'upload': 'v1-projects:project-create-upload',
}

xml_file = 'testing/xml/project.xml'


@pytest.mark.parametrize('username', users)
@pytest.mark.parametrize('plugin_key', plugin_keys)
def test_get(db, client, login, username, plugin_key):
    login(username)

    url = reverse(urlnames['import'], args=[plugin_key])
    response = client.get(url)

    if username == 'anonymous':
        assert response.status_code == 401
    else:
        assert response.status_code == (404 if plugin_key in plugin_upload else 200)


@pytest.mark.parametrize('username', users)
@pytest.mark.parametrize('plugin_key', plugin_keys)
def test_post(db, client, login, username, plugin_key):
    login(username)

    url = reverse(urlnames['import'], args=[plugin_key])
    response = client.post(url)

    if username == 'anonymous':
        assert response.status_code == 401
    else:
        assert response.status_code == (404 if plugin_key in plugin_upload else 200)


@pytest.mark.parametrize('username', users)
def test_upload(db, client, login, username):
    login(username)

    url = reverse(urlnames['upload'])
    with open(xml_file, 'rb') as fp:
        response = client.post(url, {'uploaded_file': fp})

    if username == 'anonymous':
        assert response.status_code == 401
    else:
        assert response.status_code == 200
        assert response.json()['key'] == 'xml'


def test_upload_no_file(db, client, login):
    login('user')

    url = reverse(urlnames['upload'])
    response = client.post(url)

    assert response.status_code == 400
    assert 'uploaded_file' in response.json()


def test_upload_unknown_file(db, client, login):
    login('user')

    url = reverse(urlnames['upload'])
    response = client.post(url, {'uploaded_file': SimpleUploadedFile('project.txt', b'not a project')})

    assert response.status_code == 400
    assert 'uploaded_file' in response.json()


def test_upload_restricted(db, client, login, settings):
    settings.PROJECT_CREATE_RESTRICTED = True
    login('user')

    url = reverse(urlnames['upload'])
    with open(xml_file, 'rb') as fp:
        response = client.post(url, {'uploaded_file': fp})

    assert response.status_code == 403

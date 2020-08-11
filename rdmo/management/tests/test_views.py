import os

import pytest
from django.urls import reverse

from rdmo.core.xml import flat_xml_to_elements, read_xml_file

users = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('api', 'api'),
    ('anonymous', None),
)

files = (
    'conditions.xml',
    'domain.xml',
    'options.xml',
    'questions.xml',
    'tasks.xml',
    'views.xml'
)

status_map = {
    'upload_get': {
        'editor': 302, 'reviewer': 302, 'api': 302, 'user': 302, 'anonymous': 302
    },
    'upload_post': {
        'editor': 200, 'reviewer': 403, 'api': 200, 'user': 403, 'anonymous': 302
    },
    'upload_post_empty': {
        'editor': 302, 'reviewer': 302, 'api': 302, 'user': 302, 'anonymous': 302
    },
    'upload_post_error': {
        'editor': 400, 'reviewer': 400, 'api': 400, 'user': 400, 'anonymous': 302
    },
    'import_get': {
        'editor': 302, 'reviewer': 302, 'api': 302, 'user': 302, 'anonymous': 302
    },
    'import_post': {
        'editor': 200, 'reviewer': 403, 'api': 200, 'user': 403, 'anonymous': 302
    },
    'import_post_empty': {
        'editor': 302, 'reviewer': 403, 'api': 302, 'user': 403, 'anonymous': 302
    },
    'import_post_error': {
        'editor': 400, 'reviewer': 400, 'api': 400, 'user': 400, 'anonymous': 302
    }
}


@pytest.mark.parametrize('username,password', users)
def test_upload_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('upload')
    response = client.get(url)

    assert response.status_code == status_map['upload_get'][username], response.content

    if not password:
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('file_name', files)
@pytest.mark.parametrize('username,password', users)
def test_upload_post_conditions(db, settings, client, username, password, file_name):
    client.login(username=username, password=password)

    xml_file = os.path.join(settings.BASE_DIR, 'xml', file_name)

    url = reverse('upload')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    assert response.status_code == status_map['upload_post'][username]

    if not password:
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_upload_post_empty(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('upload')
    response = client.post(url)

    assert response.status_code == status_map['upload_post_empty'][username]

    if not password:
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_upload_post_error(db, settings, client, username, password):
    client.login(username=username, password=password)

    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'error.xml')

    url = reverse('upload')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    assert response.status_code == status_map['upload_post_error'][username]

    if not password:
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_import_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('import')
    response = client.get(url)

    assert response.status_code == status_map['import_get'][username], response.content

    if not password:
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('file_name', files)
@pytest.mark.parametrize('username,password', users)
def test_import_post(db, settings, client, username, password, file_name):
    client.login(username=username, password=password)

    xml_file = os.path.join(settings.BASE_DIR, 'xml', file_name)

    session = client.session
    session['import_file_name'] = file_name
    session['import_tmpfile_name'] = xml_file
    session.save()

    root = read_xml_file(xml_file)
    elements = flat_xml_to_elements(root)
    checked = [element.get('uri') for element in elements]
    data = {uri: ['on'] for uri in checked}

    url = reverse('import')
    response = client.post(url, data)

    assert response.status_code == status_map['import_post'][username]

    if not password:
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('file_name', files)
@pytest.mark.parametrize('username,password', users)
def test_import_post_empty(db, settings, client, username, password, file_name):
    client.login(username=username, password=password)

    xml_file = os.path.join(settings.BASE_DIR, 'xml', file_name)

    session = client.session
    session['import_file_name'] = file_name
    session['import_tmpfile_name'] = xml_file
    session.save()

    url = reverse('import')
    response = client.post(url)

    assert response.status_code == status_map['import_post_empty'][username]

    if not password:
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_import_post_error(db, settings, client, username, password):
    client.login(username=username, password=password)

    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'error.xml')

    session = client.session
    session['import_file_name'] = 'error.xml'
    session['import_tmpfile_name'] = xml_file
    session.save()

    url = reverse('import')
    response = client.post(url)

    assert response.status_code == status_map['import_post_error'][username]

    if not password:
        assert response.url.startswith('/account/login/'), response.content

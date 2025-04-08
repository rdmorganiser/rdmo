from pathlib import Path

import pytest

from django.conf import settings
from django.urls import reverse

from rdmo.questions.models import Catalog, Page, Question, QuestionSet, Section

from .helpers_xml import xml_error_files

users = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('api', 'api'),
    ('anonymous', None),
)

status_map = {
    'list': {
        'editor': 405, 'reviewer': 405, 'api': 405, 'user': 405, 'anonymous': 401
    },
    'create': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 200, 'anonymous': 401
    },
    'create_error': {
        'editor': 400, 'reviewer': 400, 'api': 400, 'user': 400, 'anonymous': 401
    }
}

urlnames = {
    'list': 'v1-management:upload-list'
}



@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'catalogs.xml'

    url = reverse(urlnames['list'])
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'file': f})

    assert response.status_code == status_map['create'][username], response.json()
    if response.status_code == 200:
        for element in response.json():
            if username in ['api', 'editor']:
                assert element.get('updated') is True
            else:
                assert element.get('updated') is False


@pytest.mark.parametrize('username,password', users)
def test_create_import_create(db, client, username, password, delete_all_objects):
    delete_all_objects(Catalog, Section, Page, QuestionSet, Question)

    client.login(username=username, password=password)

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'catalogs.xml'

    url = reverse(urlnames['list'])
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'file': f, 'import': 'true'})

    assert response.status_code == status_map['create'][username], response.json()
    if response.status_code == 200:
        for element in response.json():
            assert element.get('created') is False if username in ['reviewer', 'user'] else True
            assert element.get('updated') is False


@pytest.mark.parametrize('username,password', users)
def test_create_import_update(db, client, username, password):
    client.login(username=username, password=password)

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'catalogs.xml'

    url = reverse(urlnames['list'])
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'file': f, 'import': 'true'})

    assert response.status_code == status_map['create'][username], response.json()
    if response.status_code == 200:
        for element in response.json():
            assert element.get('created') is False
            assert element.get('updated') is False if username in ['reviewer', 'user'] else True


@pytest.mark.parametrize('username,password', users)
def test_create_empty(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.post(url, {})
    assert response.status_code == status_map['create_error'][username], response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('xml_file_path,error_message', xml_error_files.items())
def test_create_error(db, client, username, password, xml_file_path, error_message):
    client.login(username=username, password=password)

    xml_file = Path(settings.BASE_DIR).joinpath(xml_file_path)
    url = reverse(urlnames['list'])
    try:
        with open(xml_file, encoding='utf8') as f:
            response = client.post(url, {'file': f})
    except FileNotFoundError:
        # one test case is for a non-existent file
        response = client.post(url)

    assert response.status_code == status_map['create_error'][username], response.json()
    if response.status_code == 400:
        response_msg = " ".join(response.json()['file'])
        assert error_message in response_msg

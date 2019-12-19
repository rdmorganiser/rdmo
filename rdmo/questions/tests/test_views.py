import os

import pytest
from django.urls import reverse

users = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('api', 'api'),
    ('anonymous', None),
)

status_map = {
    'catalogs': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
    },
    'questions_catalog_export': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
    },
    'questions_catalog_import': {
        'editor': 302, 'reviewer': 403, 'api': 302, 'user': 403, 'anonymous': 302
    },
    'questions_catalog_import_error': {
        'editor': 400, 'reviewer': 403, 'api': 400, 'user': 403, 'anonymous': 302
    }
}

catalog_pk = 1

export_formats = ('xml', 'rtf', 'odt', 'docx', 'html', 'markdown', 'tex', 'pdf')


@pytest.mark.parametrize('username,password', users)
def test_questions(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('catalogs')
    response = client.get(url)
    assert response.status_code == status_map['catalogs'][username]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_questions_export(db, client, username, password, export_format):
    client.login(username=username, password=password)

    url = reverse('questions_catalog_export', args=[catalog_pk, export_format])
    response = client.get(url)
    assert response.status_code == status_map['questions_catalog_export'][username]


@pytest.mark.parametrize('username,password', users)
def test_questions_import_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('questions_catalog_import', args=['xml'])
    response = client.get(url)
    assert response.status_code == status_map['questions_catalog_import'][username]


@pytest.mark.parametrize('username,password', users)
def test_questions_import_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('questions_catalog_import', args=['xml'])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'questions.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})
    assert response.status_code == status_map['questions_catalog_import'][username]


@pytest.mark.parametrize('username,password', users)
def test_questions_import_empty_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('questions_catalog_import', args=['xml'])
    response = client.post(url)
    assert response.status_code == status_map['questions_catalog_import'][username]


@pytest.mark.parametrize('username,password', users)
def test_questions_import_error_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('questions_catalog_import', args=['xml'])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'error.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})
    assert response.status_code == status_map['questions_catalog_import_error'][username]

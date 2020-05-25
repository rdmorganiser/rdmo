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
    'views': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
    },
    'views_export': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
    },
    'views_import': {
        'editor': 302, 'reviewer': 403, 'api': 302, 'user': 403, 'anonymous': 302
    },
    'views_import_error': {
        'editor': 400, 'reviewer': 403, 'api': 400, 'user': 403, 'anonymous': 302
    }
}

export_formats = ('xml', 'rtf', 'odt', 'docx', 'html', 'markdown', 'tex', 'pdf')


@pytest.mark.parametrize('username,password', users)
def test_views(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('views')
    response = client.get(url)
    assert response.status_code == status_map['views'][username]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_views_export(db, client, username, password, export_format):
    client.login(username=username, password=password)

    url = reverse('views_export', args=[export_format])
    response = client.get(url)
    assert response.status_code == status_map['views_export'][username]


@pytest.mark.parametrize('username,password', users)
def test_views_import_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('views_import', args=['xml'])
    response = client.get(url)
    assert response.status_code == status_map['views_import'][username]


@pytest.mark.parametrize('username,password', users)
def test_views_import_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('views_import', args=['xml'])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'views.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})
    assert response.status_code == status_map['views_import'][username]


@pytest.mark.parametrize('username,password', users)
def test_views_import_empty_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('views_import', args=['xml'])
    response = client.post(url)
    assert response.status_code == status_map['views_import'][username]


@pytest.mark.parametrize('username,password', users)
def test_views_import_error_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('views_import', args=['xml'])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'error.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})
    assert response.status_code == status_map['views_import_error'][username]

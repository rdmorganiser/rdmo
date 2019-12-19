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
    'domain': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
    },
    'domain_export': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
    },
    'domain_import': {
        'editor': 302, 'reviewer': 403, 'api': 302, 'user': 403, 'anonymous': 302
    },
    'domain_import_error': {
        'editor': 400, 'reviewer': 403, 'api': 400, 'user': 403, 'anonymous': 302
    }
}

export_formats = ('xml', 'rtf', 'odt', 'docx', 'html', 'markdown', 'tex', 'pdf', 'csv', 'csvcomma')


@pytest.mark.parametrize('username,password', users)
def test_domain(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('domain')
    response = client.get(url)
    assert response.status_code == status_map['domain'][username]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_domain_export(db, client, username, password, export_format):
    client.login(username=username, password=password)

    url = reverse('domain_export', args=[export_format])
    response = client.get(url)
    assert response.status_code == status_map['domain_export'][username]


@pytest.mark.parametrize('username,password', users)
def test_domain_import_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('domain_import', args=['xml'])
    response = client.get(url)
    assert response.status_code == status_map['domain_import'][username]


@pytest.mark.parametrize('username,password', users)
def test_domain_import_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('domain_import', args=['xml'])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'domain.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})
    assert response.status_code == status_map['domain_import'][username]


@pytest.mark.parametrize('username,password', users)
def test_domain_import_empty_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('domain_import', args=['xml'])
    response = client.post(url)
    assert response.status_code == status_map['domain_import'][username]


@pytest.mark.parametrize('username,password', users)
def test_domain_import_error_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('domain_import', args=['xml'])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'error.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})
    assert response.status_code == status_map['domain_import_error'][username]

import xml.etree.ElementTree as et

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

    if response.status_code == 200:
        if export_format == 'xml':
            root = et.fromstring(response.content)
            assert root.tag == 'rdmo'
            for child in root:
                assert child.tag in ['attribute']

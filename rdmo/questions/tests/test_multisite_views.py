import xml.etree.ElementTree as et

import pytest
from django.urls import reverse

users = (
    ('editor', 'editor'),
    ('site', 'site'),
    ('foo-editor', 'foo-editor'),
    ('bar-editor', 'bar-editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('api', 'api'),
    ('anonymous', None),
)

status_map = {
    'catalogs': {
        'editor': 200, 'site': 200, 'foo-editor': 200, 'bar-editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
    },
    'questions_catalog_export': {
        'editor': 200, 'site': 200, 'foo-editor': 200, 'bar-editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
    }
}

catalog_pks = (1, 2, 3, 4)

export_formats = ('xml', 'rtf', 'odt', 'docx', 'html', 'markdown', 'tex', 'pdf')


@pytest.mark.parametrize('username,password', users)
def test_questions(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('catalogs')
    response = client.get(url)
    assert response.status_code == status_map['catalogs'][username]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_multisite_questions_export(db, client, username, password, export_format):
    client.login(username=username, password=password)

    for catalog_pk in catalog_pks:
        url = reverse('questions_catalog_export', args=[catalog_pk, export_format])
        response = client.get(url)
        assert response.status_code == status_map['questions_catalog_export'][username]

        if response.status_code == 200:
            if export_format == 'xml':
                root = et.fromstring(response.content)
                assert root.tag == 'rdmo'
                for child in root:
                    assert child.tag in ['catalog', 'section', 'questionset', 'question']

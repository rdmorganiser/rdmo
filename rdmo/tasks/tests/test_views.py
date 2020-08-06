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
    'tasks': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
    },
    'tasks_export': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
    }
}

export_formats = ('xml', 'rtf', 'odt', 'docx', 'html', 'markdown', 'tex', 'pdf')


@pytest.mark.parametrize('username,password', users)
def test_tasks(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('tasks')
    response = client.get(url)
    assert response.status_code == status_map['tasks'][username]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_tasks_export(db, client, username, password, export_format):
    client.login(username=username, password=password)

    url = reverse('tasks_export', args=[export_format])
    response = client.get(url)
    assert response.status_code == status_map['tasks_export'][username]

    if response.status_code == 200:
        if export_format == 'xml':
            root = et.fromstring(response.content)
            assert root.tag == 'rdmo'
            for child in root:
                assert child.tag in ['task']

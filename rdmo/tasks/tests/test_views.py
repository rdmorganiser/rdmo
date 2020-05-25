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
    'tasks': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
    },
    'tasks_export': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
    },
    'tasks_import': {
        'editor': 302, 'reviewer': 403, 'api': 302, 'user': 403, 'anonymous': 302
    },
    'tasks_import_error': {
        'editor': 400, 'reviewer': 403, 'api': 400, 'user': 403, 'anonymous': 302
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


@pytest.mark.parametrize('username,password', users)
def test_tasks_import_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('tasks_import', args=['xml'])
    response = client.get(url)
    assert response.status_code == status_map['tasks_import'][username]


@pytest.mark.parametrize('username,password', users)
def test_tasks_import_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('tasks_import', args=['xml'])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'tasks.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})
    assert response.status_code == status_map['tasks_import'][username]


@pytest.mark.parametrize('username,password', users)
def test_tasks_import_empty_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('tasks_import', args=['xml'])
    response = client.post(url)
    assert response.status_code == status_map['tasks_import'][username]


@pytest.mark.parametrize('username,password', users)
def test_tasks_import_error_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('tasks_import', args=['xml'])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'error.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})
    assert response.status_code == status_map['tasks_import_error'][username]

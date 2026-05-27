
import xml.etree.ElementTree as et

import pytest

from django.urls import reverse

from ..models import Plugin

users = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('api', 'api'),
    ('anonymous', None),
)

status_map = {
    'list': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 401
    },
    'detail': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 404, 'anonymous': 401
    },
    'create': {
        'editor': 201, 'reviewer': 403, 'api': 201, 'user': 403, 'anonymous': 401
    },
    'update': {
        'editor': 200, 'reviewer': 403, 'api': 200, 'user': 404, 'anonymous': 401
    },
    'delete': {
        'editor': 204, 'reviewer': 403, 'api': 204, 'user': 404, 'anonymous': 401
    }
}

urlnames = {
    'list': 'v1-config:plugin-list',
    'index': 'v1-config:plugin-index',
    'detail': 'v1-config:plugin-detail',
    'export': 'v1-config:plugin-export',
    'detail_export': 'v1-config:plugin-detail-export',
}

export_formats = ('xml', 'html')


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_index(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['index'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_export(db, client, username, password, export_format):
    client.login(username=username, password=password)

    url = reverse(urlnames['export']) + export_format + '/'
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.content

    if response.status_code == 200 and export_format == 'xml':
        root = et.fromstring(response.content)
        assert root.tag == 'rdmo'
        for child in root:
            assert child.tag in ['plugin']


def test_export_search(db, client):
    client.login(username='editor', password='editor')

    url = reverse(urlnames['export']) + 'xml/?search=testing'
    response = client.get(url)
    assert response.status_code == status_map['list']['editor'], response.content


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Plugin.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_detail_export(db, client, username, password, export_format):
    client.login(username=username, password=password)
    instance = Plugin.objects.first()

    url = reverse(urlnames['detail_export'], args=[instance.pk]) + export_format + '/'
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content

    if response.status_code == 200 and export_format == 'xml':
        root = et.fromstring(response.content)
        assert root.tag == 'rdmo'
        for child in root:
            assert child.tag in ['plugin']


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Plugin.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': f'{instance.uri_path}_new_{username}',
            'comment': instance.comment,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'help_en': instance.help_lang1,
            'help_de': instance.help_lang2,
            'python_path': instance.python_path,
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Plugin.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'help_en': instance.help_lang1,
            'help_de': instance.help_lang2,
            'python_path': instance.python_path,
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()


@pytest.mark.parametrize('python_path', [
    'rdmo.projects.exports.JSONExport',
    'this.python.path.DoesNotExist',
])
@pytest.mark.parametrize('is_in_plugins', [ True, False ])
def test_update_python_path(db, client, settings, python_path, is_in_plugins):
    client.login(username='editor', password='editor')
    instance = Plugin.objects.filter(python_path__contains='XMLExport').first()
    assert instance.python_path != python_path  # check for arrangement
    if is_in_plugins:
        settings.PLUGINS = [instance.python_path, python_path]
        assert python_path in settings.PLUGINS  # check for arrangement
    else:
        settings.PLUGINS = [instance.python_path]
        assert python_path not in settings.PLUGINS  # check for arrangement

    url = reverse(urlnames['detail'], args=[instance.pk])
    data = {
        'uri_prefix': instance.uri_prefix,
        'uri_path': instance.uri_path,
        'comment': instance.comment,
        'title_en': instance.title_lang1,
        'title_de': instance.title_lang2,
        'help_en': instance.help_lang1,
        'help_de': instance.help_lang2,
        'python_path': python_path,
    }

    response = client.put(url, data, content_type='application/json')
    if 'DoesNotExist' in python_path:
        assert response.status_code == 400, response.json()
        assert "not a valid choice" in response.json()['python_path'][0]

        instance.refresh_from_db()
        assert instance.python_path == instance.python_path  # nothing changed
    elif is_in_plugins:
        assert response.status_code == 200, response.json()
        assert response.json()['python_path'] == python_path

        instance.refresh_from_db()
        assert instance.python_path == python_path
    else:
        assert response.status_code == 400, response.json()
        assert 'This path is not in the configured paths.' in response.json()['python_path']

        instance.refresh_from_db()
        assert instance.python_path == instance.python_path  # nothing changed


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Plugin.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()

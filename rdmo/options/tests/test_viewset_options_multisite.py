import xml.etree.ElementTree as et

import pytest
from django.contrib.sites.models import Site
from django.urls import reverse

from ..models import Option


users = (
    ('editor', 'editor'),
    ('user', 'user'),
    ('example-reviewer', 'example-reviewer'),
    ('example-editor', 'example-editor'),
    ('foo-user', 'foo-user'),
    ('foo-reviewer', 'foo-reviewer'),
    ('foo-editor', 'foo-editor'),
    ('bar-user', 'bar-user'),
    ('bar-reviewer', 'bar-reviewer'),
    ('bar-editor', 'bar-editor'),
)


status_map = {
    'list': {
        'foo-user': 403, 'foo-reviewer': 200, 'foo-editor': 200,
        'bar-user': 403, 'bar-reviewer': 200, 'bar-editor': 200,
        'user': 403, 'example-reviewer': 200, 'example-editor': 200,
        'editor': 200
    },
    'detail': {
        'foo-user': 404, 'foo-reviewer': 200, 'foo-editor': 200,
        'bar-user': 404, 'bar-reviewer': 200, 'bar-editor': 200,
        'user': 404, 'example-reviewer': 200, 'example-editor': 200,
        'editor': 200
    },
    'create': {
        'foo-user': 403, 'foo-reviewer': 403, 'foo-editor': 201,
        'bar-user': 403, 'bar-reviewer': 403, 'bar-editor': 201,
        'user': 403, 'example-reviewer': 403, 'example-editor': 201,
        'editor': 201
    },
    'copy': {
        'foo-user': 404, 'foo-reviewer': 403, 'foo-editor': 201,
        'bar-user': 404, 'bar-reviewer': 403, 'bar-editor': 201,
        'user': 404, 'example-reviewer': 403, 'example-editor': 201,
        'editor': 201
    },
    'update': {
        'foo-user': 404, 'foo-reviewer': 403, 'foo-editor': 200,
        'bar-user': 404, 'bar-reviewer': 403, 'bar-editor': 200,
        'user': 404, 'example-reviewer': 403, 'example-editor': 200,
        'editor': 200
    },
    'delete': {
        'foo-user': 404, 'foo-reviewer': 404, 'foo-editor': 404,
        'bar-user': 404, 'bar-reviewer': 404, 'bar-editor': 404,
        'user': 404, 'example-reviewer': 403, 'example-editor': 204,
        'editor': 204
    }
}


status_map_object_permissions = {
    'copy': {
        'foo-option-1': {
            'foo-reviewer': 403, 'foo-editor': 201,
            'bar-reviewer': 404, 'bar-editor': 404,
            'example-reviewer': 404, 'example-editor': 404,
        },
        'bar-option-1': {
            'foo-reviewer': 404, 'foo-editor': 404,
            'bar-reviewer': 403, 'bar-editor': 201,
            'example-reviewer': 404, 'example-editor': 404,
        }
    },
    'update': {
        'foo-option-1': {
            'foo-reviewer': 403, 'foo-editor': 200,
            'bar-reviewer': 404, 'bar-editor': 404,
            'example-reviewer': 404, 'example-editor': 404,
        },
        'bar-option-1': {
            'foo-reviewer': 404, 'foo-editor': 404,
            'bar-reviewer': 403, 'bar-editor': 200,
            'example-reviewer': 404, 'example-editor': 404,
        }
    },
    'delete': {
        'foo-option-1': {
            'foo-reviewer': 403, 'foo-editor': 204,
            'bar-reviewer': 404, 'bar-editor': 404,
            'example-reviewer': 404, 'example-editor': 404,
        },
        'bar-option-1': {
            'foo-reviewer': 404, 'foo-editor': 404,
            'bar-reviewer': 403, 'bar-editor': 204,
            'example-reviewer': 404, 'example-editor': 404,
        }
    },
}

def get_status_map_or_obj_perms(instance, username, method):
    ''' looks for the object permissions of the instance and returns the status code '''
    if instance.editors.exists():
        try:
            if instance.uri_path.endswith('-option-2') and (instance.uri_path.startswith('foo') or instance.uri_path.startswith('bar')):
                return status_map_object_permissions[method][instance.uri_path.replace('-2', '-1')][username]
            return status_map_object_permissions[method][instance.uri_path][username]
        except KeyError:
            return status_map[method][username]
    else:
        return status_map[method][username]


urlnames = {
    'list': 'v1-options:option-list',
    'index': 'v1-options:option-index',
    'export': 'v1-options:option-export',
    'detail': 'v1-options:option-detail',
    'detail_export': 'v1-options:option-detail-export',
    'copy': 'v1-options:option-copy'
}


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
def test_export(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['export'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.content

    if response.status_code == 200:
        root = et.fromstring(response.content)
        assert root.tag == 'rdmo'
        for child in root:
            assert child.tag in ['option']


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Option.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Option.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'key': '%s_new_%s' % (instance.key, username),
            'comment': instance.comment,
            'optionset': instance.optionset.pk,
            'order': instance.order,
            'text_en': instance.text_lang1,
            'text_de': instance.text_lang2
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_update_multisite(db, client, username, password):
    client.login(username=username, password=password)
    instances = Option.objects.all()

    for instance in instances:
        optionsets = [optionset.id for optionset in instance.optionsets.all()]

        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'text_en': instance.text_lang1,
            'text_de': instance.text_lang2
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == get_status_map_or_obj_perms(instance, username, 'update'), response.json()

        instance.refresh_from_db()
        assert optionsets == [optionset.id for optionset in instance.optionsets.all()]


@pytest.mark.parametrize('username,password', users)
def test_delete_multisite(db, client, username, password):
    client.login(username=username, password=password)
    instances = Option.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == get_status_map_or_obj_perms(instance, username, 'delete'), response.json()


@pytest.mark.parametrize('username,password', users)
def test_copy_multisite(db, client, username, password):
    client.login(username=username, password=password)
    instances = Option.objects.all()

    for instance in instances:
        url = reverse(urlnames['copy'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix + '-',
            'uri_path': instance.uri_path + '-'
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == get_status_map_or_obj_perms(instance, username, 'copy'), response.json()


@pytest.mark.parametrize('username,password', users)
def test_copy_wrong(db, client, username, password):
    client.login(username=username, password=password)
    instance = Option.objects.first()

    url = reverse(urlnames['copy'], args=[instance.pk])
    data = {
        'uri_prefix': instance.uri_prefix,
        'key': instance.key
    }
    response = client.put(url, data, content_type='application/json')

    if status_map['copy'][username] == 201:
        assert response.status_code == 400, response.json()
    else:
        assert response.status_code == status_map['copy'][username], response.json()

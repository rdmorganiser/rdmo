import xml.etree.ElementTree as et

import pytest
from django.contrib.sites.models import Site
from django.urls import reverse

from ..models import OptionSet

from .test_viewset_optionsets import export_formats


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
        'foo-user': 404, 'foo-reviewer': 403, 'foo-editor': 204,
        'bar-user': 404, 'bar-reviewer': 403, 'bar-editor': 204,
        'user': 404, 'example-reviewer': 403, 'example-editor': 204,
        'editor': 204
    }
}


status_map_object_permissions = {
    'copy': {
        'foo-optionset': {
            'foo-reviewer': 403, 'foo-editor': 201,
            'bar-reviewer': 404, 'bar-editor': 404,
            'example-reviewer': 404, 'example-editor': 404,
        },
        'bar-optionset': {
            'foo-reviewer': 404, 'foo-editor': 404,
            'bar-reviewer': 403, 'bar-editor': 201,
            'example-reviewer': 404, 'example-editor': 404,
        }
    },
    'update': {
        'foo-optionset': {
            'foo-reviewer': 403, 'foo-editor': 200,
            'bar-reviewer': 404, 'bar-editor': 404,
            'example-reviewer': 404, 'example-editor': 404,
        },
        'bar-optionset': {
            'foo-reviewer': 404, 'foo-editor': 404,
            'bar-reviewer': 403, 'bar-editor': 200,
            'example-reviewer': 404, 'example-editor': 404,
        }
    },
    'delete': {
        'foo-optionset': {
            'foo-reviewer': 403, 'foo-editor': 204,
            'bar-reviewer': 404, 'bar-editor': 404,
            'example-reviewer': 404, 'example-editor': 404,
        },
        'bar-optionset': {
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
            return status_map_object_permissions[method][instance.uri_path][username]
        except KeyError:
            return status_map[method][username]
    else:
        return status_map[method][username]


urlnames = {
    'list': 'v1-options:optionset-list',
    'nested': 'v1-options:optionset-nested',
    'index': 'v1-options:optionset-index',
    'export': 'v1-options:optionset-export',
    'detail': 'v1-options:optionset-detail',
    'detail_export': 'v1-options:optionset-detail-export',
    'copy': 'v1-options:optionset-copy'
}


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_nested(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['nested'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


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
            assert child.tag in ['optionset', 'option']


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': '%s_new_%s' % (instance.uri_path, username),
            'comment': instance.comment,
            'order': instance.order,
            'conditions': [condition.pk for condition in instance.conditions.all()],
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_update_m2m_multisite(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        optionset_options = [{
            'option': optionset_option.option.id,
            'order': optionset_option.order
        } for optionset_option in instance.optionset_options.all()[:1]]
        conditions = [condition.pk for condition in instance.conditions.all()[:1]]

        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'order': instance.order,
            'options': optionset_options,
            'conditions': conditions,
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == get_status_map_or_obj_perms(instance, username, 'update'), response.json()

        if response.status_code == 200:
            instance.refresh_from_db()
            assert optionset_options == [{
                'option': optionset_option.option.id,
                'order': optionset_option.order
            } for optionset_option in instance.optionset_options.all()]
            assert conditions == [condition.pk for condition in instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_delete_multisite(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == get_status_map_or_obj_perms(instance, username, 'delete'), response.json()


@pytest.mark.parametrize('username,password', users)
def test_detail_export(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail_export'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.content

        if response.status_code == 200:
            root = et.fromstring(response.content)
            assert root.tag == 'rdmo'
            for child in root:
                assert child.tag in ['optionset', 'option']


@pytest.mark.parametrize('username,password', users)
def test_copy_multisite(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

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
    instance = OptionSet.objects.first()

    url = reverse(urlnames['copy'], args=[instance.pk])
    data = {
        'uri_prefix': instance.uri_prefix,
        'uri_path': instance.uri_path
    }
    response = client.put(url, data, content_type='application/json')

    if status_map['copy'][username] == 201:
        assert response.status_code == 400, response.json()
    else:
        assert response.status_code == status_map['copy'][username], response.json()
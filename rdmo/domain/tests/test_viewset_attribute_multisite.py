import xml.etree.ElementTree as et

import pytest

from django.urls import reverse

from rdmo.core.tests.constants import multisite_status_map as status_map
from rdmo.core.tests.constants import multisite_users as users

from ..models import Attribute
from .test_viewset_attribute import urlnames

STATUS_CODES = {
    'nested': {
        'https://foo.com/terms/domain/foo-attribute': {
            'user': 404, 'reviewer': 200, 'editor': 200,
            'example-reviewer': 200, 'example-editor': 200, 'foo-user': 404,
            'foo-reviewer': 200, 'foo-editor': 200, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://bar.com/terms/domain/bar-attribute': {
            'user': 404, 'reviewer': 200, 'editor': 200,
            'example-reviewer': 200, 'example-editor': 200, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 200, 'bar-editor': 200, 'anonymous': 401,
        },
    },
    'detail': {
        'https://foo.com/terms/domain/foo-attribute': {
            'user': 404, 'reviewer': 200, 'editor': 200,
            'example-reviewer': 200, 'example-editor': 200, 'foo-user': 404,
            'foo-reviewer': 200, 'foo-editor': 200, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://bar.com/terms/domain/bar-attribute': {
            'user': 404, 'reviewer': 200, 'editor': 200,
            'example-reviewer': 200, 'example-editor': 200, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 200, 'bar-editor': 200, 'anonymous': 401,
        },
    },
    'update': {
        'https://foo.com/terms/domain/foo-attribute': {
            'user': 404, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 403, 'foo-editor': 200, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://bar.com/terms/domain/bar-attribute': {
            'user': 404, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 403, 'bar-editor': 200, 'anonymous': 401,
        },
    },
    'delete': {
        'https://foo.com/terms/domain/foo-attribute': {
            'user': 404, 'reviewer': 403, 'editor': 204,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 403, 'foo-editor': 204, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://bar.com/terms/domain/bar-attribute': {
            'user': 404, 'reviewer': 403, 'editor': 204,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 403, 'bar-editor': 204, 'anonymous': 401,
        },
    },
}



@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_nested(db, client, username, password):
    ''' only users and status_map are unique for this test '''
    client.login(username=username, password=password)
    instances = Attribute.objects.order_by('-level')

    for instance in instances:
        url = reverse(urlnames['nested'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == STATUS_CODES['nested'].get(instance.uri, status_map['nested'])[username], (
            response.json()
        )


@pytest.mark.parametrize('username,password', users)
def test_export(db, client, username, password):
    ''' only users and status_map are unique for this test '''
    client.login(username=username, password=password)

    url = reverse(urlnames['export'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.content

    if response.status_code == 200:
        root = et.fromstring(response.content)
        assert root.tag == 'rdmo'
        for child in root:
            assert child.tag in ['attribute']


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    ''' only users and status_map are unique for this test '''
    client.login(username=username, password=password)
    instances = Attribute.objects.order_by('-level')

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == (
            STATUS_CODES['detail'].get(instance.uri, status_map['detail'])[username]
        ), response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    ''' only users and status_map are unique for this test '''
    client.login(username=username, password=password)
    instances = Attribute.objects.order_by('-level')

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'key': f'{instance.key}_new_{username}',
            'comment': '',
            'parent': instance.parent.pk if instance.parent else ''
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Attribute.objects.order_by('-level')

    for instance in instances:

        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'key': instance.key,
            'comment': '',
            'parent': instance.parent.pk if instance.parent else ''
        }
        response = client.put(url, data, content_type='application/json')

        assert response.status_code == (
            STATUS_CODES['update'].get(instance.uri, status_map['update'])[username]
        ), response.json()


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Attribute.objects.order_by('-level')

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == STATUS_CODES['delete'].get(instance.uri, status_map['delete'])[username]


@pytest.mark.parametrize('username,password', users)
def test_detail_export(db, client, username, password):
    client.login(username=username, password=password)
    instances = Attribute.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail_export'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == (
            STATUS_CODES['detail'].get(instance.uri, status_map['detail'])[username]
        ), response.json()

        if response.status_code == 200:
            root = et.fromstring(response.content)
            assert root.tag == 'rdmo'
            for child in root:
                assert child.tag in ['attribute']

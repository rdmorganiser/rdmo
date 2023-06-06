import xml.etree.ElementTree as et

import pytest
from django.urls import reverse
from django.contrib.sites.models import Site

from ..models import Condition

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
    ('anonymous', None),
)


status_map = {
    'list': {
        'foo-user': 403, 'foo-reviewer': 200, 'foo-editor': 200,
        'bar-user': 403, 'bar-reviewer': 200, 'bar-editor': 200,
        'user': 403, 'example-reviewer': 200, 'example-editor': 200,
        'editor': 200,
        'anonymous': 401
    },
    'detail': {
        'foo-user': 404, 'foo-reviewer': 200, 'foo-editor': 200,
        'bar-user': 404, 'bar-reviewer': 200, 'bar-editor': 200,
        'user': 404, 'example-reviewer': 200, 'example-editor': 200,
        'editor': 200,
        'anonymous': 401
    },
    'create': {
        'foo-user': 403, 'foo-reviewer': 403, 'foo-editor': 201,
        'bar-user': 403, 'bar-reviewer': 403, 'bar-editor': 201,
        'user': 403, 'example-reviewer': 403, 'example-editor': 201,
        'editor': 201,
        'anonymous': 401
    },
    'update': {
        'foo-user': 404, 'foo-reviewer': 403, 'foo-editor': 200,
        'bar-user': 404, 'bar-reviewer': 403, 'bar-editor': 200,
        'user': 404, 'example-reviewer': 403, 'example-editor': 200,
        'editor': 200,
        'anonymous': 401
    },
    'delete': {
        'foo-user': 404, 'foo-reviewer': 403, 'foo-editor': 204,
        'bar-user': 404, 'bar-reviewer': 403, 'bar-editor': 204,
        'user': 404, 'example-reviewer': 403, 'example-editor': 204,
        'editor': 204,
        'anonymous': 401
    }
}

status_map_multisite_editors = {
    'example.com': ['example-editor', 'editor'],
    'foo.com': ['foo-editor'],
    'bar.com': ['bar-editor'],
    
}

urlnames = {
    'list': 'v1-conditions:condition-list',
    'index': 'v1-conditions:condition-index',
    'export': 'v1-conditions:condition-export',
    'detail': 'v1-conditions:condition-detail',
    'detail_export': 'v1-conditions:condition-detail-export',
    'copy': 'v1-conditions:condition-copy'
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
            assert child.tag in ['condition']


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'key': '%s_new_%s' % (instance.key, username),
            'comment': instance.comment,
            'source': instance.source.pk,
            'relation': instance.relation,
            'target_text': instance.target_text,
            'target_option': instance.target_option.pk if instance.target_option else ''
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        
        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'key': instance.key + '-' + username,
            'comment': instance.comment,
            'source': instance.source.pk,
            'relation': instance.relation,
            'target_text': instance.target_text,
            'target_option': instance.target_option.pk if instance.target_option else None
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def _skip_test_update_with_editors_currentsite(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        
        # set current site for object permissions, example-com
        instance.editors.set([Site.objects.get_current()])
        
        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'key': instance.key + '-' + username,
            'comment': instance.comment,
            'source': instance.source.pk,
            'relation': instance.relation,
            'target_text': instance.target_text,
            'target_option': instance.target_option.pk if instance.target_option else None
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:

        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def _skip_test_delete_with_editors_currentsite(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:

        # set current site for object permissions (=example.com)
        instance.editors.set([Site.objects.get_current()])

        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_detail_export(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail_export'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.content

        if response.status_code == 200:
            root = et.fromstring(response.content)
            assert root.tag == 'rdmo'
            for child in root:
                assert child.tag in ['condition']


@pytest.mark.parametrize('username,password', users)
def test_copy(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()
    status_map_method = 'create'
    if not 'editor' in username:
        status_map_method = 'update'

    for instance in instances:
        url = reverse(urlnames['copy'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix + '-',
            'key': instance.key + '-'
        }
        response = client.put(url, data, content_type='application/json')
        
            
        assert response.status_code == status_map[status_map_method][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_copy_wrong(db, client, username, password):
    client.login(username=username, password=password)
    instance = Condition.objects.first()

    status_map_method = 'create'
    if not 'editor' in username:
        status_map_method = 'update'


    url = reverse(urlnames['copy'], args=[instance.pk])
    data = {
        'uri_prefix': instance.uri_prefix,
        'key': instance.key
    }
    response = client.put(url, data, content_type='application/json')

    if status_map['create'][username] == 201:
        assert response.status_code == 400, response.json()
    else:
        assert response.status_code == status_map[status_map_method][username], response.json()

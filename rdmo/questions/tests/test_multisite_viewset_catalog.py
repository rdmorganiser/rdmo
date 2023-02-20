import xml.etree.ElementTree as et

import pytest
from django.urls import reverse
from django.test import TestCase

from ..models import Catalog

other_users = (
    ('user', 'user'),
    ('anonymous', None),
    ('site', 'site'),  # site manager for example.com 
    ('editor', 'editor'), # editor for all sites
    ('reviewer', 'reviewer'), # reviewer for all sites
)

groups = ( # TODO will be removed in future
    ('api', 'api'),
)


users_site_editor = (
    ('example-editor', 'example-editor'),  # can edit catalogs of example.com
    ('foo-editor', 'foo-editor'),  # can edit catalogs of foo.com
    ('bar-editor', 'bar-editor'),  # can edit catalogs of bar.com
)

users = other_users + users_site_editor

editor_users_per_site = {
    'example.com': {
        'editor': (('example-editor', 'example-editor'), )
        },
    'foo.com': {
        'editor': (('foo-editor', 'foo-editor'), )
    },
    'bar.com': {
        'editor': (('bar-editor', 'bar-editor'), )
    }
}


status_map = {
    'list': {
        'user': 403, 'site': 403, 'editor': 200, 'reviewer': 200, 'example-editor': 200, 'foo-editor': 200, 'bar-editor': 200, 'anonymous': 401
    },
    'detail': {
        'user': 403, 'site': 403, 'editor': 200, 'reviewer': 200, 'example-editor': 200, 'foo-editor': 200, 'bar-editor': 200, 'anonymous': 401
    },
    'create': {
        'user': 403, 'site': 403, 'editor': 201, 'reviewer': 403, 'example-editor': 201, 'foo-editor': 201, 'bar-editor': 201, 'anonymous': 401
    },
    'update': {
        'user': 403, 'site': 403, 'editor': 200, 'reviewer': 403, 'anonymous': 401
    },
    'delete': {
        'user': 403, 'site': 403, 'editor': 204, 'reviewer': 403, 'anonymous': 401
    }
}

status_map_obj_perms = {
    'update': {
        'catalog': {
            'example-editor': 200, 'foo-editor': 200, 'bar-editor': 200
        },
        'catalog2': {
            'example-editor': 200, 'foo-editor': 403, 'bar-editor': 403
        },
        'foo-catalog': {
            'example-editor': 403, 'foo-editor': 200, 'bar-editor': 403
        },
        'bar-catalog': {
            'example-editor': 403, 'foo-editor': 403, 'bar-editor': 200
        },
    },
    'delete': {
        'catalog': {
            'example-editor': 204, 'foo-editor': 204, 'bar-editor': 204
        },
        'catalog2': {
            'example-editor': 204, 'foo-editor': 403, 'bar-editor': 403
        },
        'foo-catalog': {
            'example-editor': 403, 'foo-editor': 204, 'bar-editor': 403
        },
        'bar-catalog': {
            'example-editor': 403, 'foo-editor': 403, 'bar-editor': 204
        },
    }
}

def get_status_code_for_catalog(username: str, 
                                catalog_key: int,
                                method: str, 
                                status_map: dict,
                                status_map_obj_perms: dict) -> int:
    test_status_user = status_map[method].get(username, None)
    if test_status_user is None:
        test_status_user = status_map_obj_perms[method][catalog_key][username]
        print(f'catalog_key: {catalog_key}, username: {username}, method: {method}, test_status_user: {test_status_user}')
    return test_status_user

#  catalog_user_combinations = [(user, passw, cat) for user,passw in users for cat in  Catalog.objects.all()]

urlnames = {
    'list': 'v1-questions:catalog-list',
    'nested': 'v1-questions:catalog-nested',
    'index': 'v1-questions:catalog-index',
    'export': 'v1-questions:catalog-export',
    'detail': 'v1-questions:catalog-detail',
    'detail_export': 'v1-questions:catalog-detail-export',
    'copy': 'v1-questions:catalog-copy'
}


class TestSiteEditorsViewSetCatalogs(TestCase):

    def setUp(self) -> None:
        Catalog.objects.get_or_create()
        return super().setUp()


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
            assert child.tag in ['catalog', 'section', 'questionset', 'question']


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_nested(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        url = reverse(urlnames['nested'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'key': '%s_new_%s' % (instance.key, username),
            'comment': instance.comment,
            'order': instance.order,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username, password', users)
def test_multisite_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()
    method = 'update'

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'key': instance.key,
            'comment': instance.comment,
            'order': instance.order,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2
        }

        test_status_user = get_status_code_for_catalog(username,
                                                       instance.key,
                                                       method,
                                                       status_map,
                                                       status_map_obj_perms)
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == test_status_user, response.json()


@pytest.mark.parametrize('username,password', users)
def test_multisite_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()
    method = 'delete'

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        test_status_user = get_status_code_for_catalog(username,
                                                       instance.key,
                                                       method,
                                                       status_map,
                                                       status_map_obj_perms)
        if test_status_user == 204 and response.status_code == 403:
            breakpoint()
        assert response.status_code == test_status_user

@pytest.mark.parametrize('username,password', users)
def test_multisite_detail_export(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail_export'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['list'][username], response.content

        if response.status_code == 200:
            root = et.fromstring(response.content)
            assert root.tag == 'rdmo'
            for child in root:
                assert child.tag in ['catalog', 'section', 'questionset', 'question']


@pytest.mark.parametrize('username,password', users)
def test_multisite_copy(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        url = reverse(urlnames['copy'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix + '-',
            'key': instance.key + '-',
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()

@pytest.mark.parametrize('username,password', users)
def test_multisitecopy_wrong(db, client, username, password):
    client.login(username=username, password=password)
    instance = Catalog.objects.first()

    url = reverse(urlnames['copy'], args=[instance.pk])
    data = {
        'uri_prefix': instance.uri_prefix,
        'key': instance.key
    }
    response = client.put(url, data, content_type='application/json')

    if status_map['create'][username] == 201:
        assert response.status_code == 400, response.json()
    else:
        assert response.status_code == status_map['create'][username], response.json()

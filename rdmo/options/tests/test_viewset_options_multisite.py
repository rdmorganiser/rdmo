import xml.etree.ElementTree as et

import pytest

from django.db.models import Max
from django.urls import reverse

from rdmo.core.tests.constants import multisite_status_map as status_map
from rdmo.core.tests.constants import multisite_users as users

from ..models import Option, OptionSet
from .test_viewset_options import urlnames

STATUS_CODES = {
    'detail': {
        'https://foo.com/terms/options/foo-option-1': {
            'user': 404, 'reviewer': 200, 'editor': 200,
            'example-reviewer': 200, 'example-editor': 200, 'foo-user': 404,
            'foo-reviewer': 200, 'foo-editor': 200, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://foo.com/terms/options/foo-option-2': {
            'user': 404, 'reviewer': 200, 'editor': 200,
            'example-reviewer': 200, 'example-editor': 200, 'foo-user': 404,
            'foo-reviewer': 200, 'foo-editor': 200, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://bar.com/terms/options/bar-option-1': {
            'user': 404, 'reviewer': 200, 'editor': 200,
            'example-reviewer': 200, 'example-editor': 200, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 200, 'bar-editor': 200, 'anonymous': 401,
        },
        'https://bar.com/terms/options/bar-option-2': {
            'user': 404, 'reviewer': 200, 'editor': 200,
            'example-reviewer': 200, 'example-editor': 200, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 200, 'bar-editor': 200, 'anonymous': 401,
        },
    },
    'create-with-parent': {
        'https://foo.com/terms/options/foo-optionset': {
            'user': 403, 'reviewer': 403, 'editor': 201,
            'example-reviewer': 403, 'example-editor': 403, 'foo-user': 403,
            'foo-reviewer': 403, 'foo-editor': 403, 'bar-user': 403,
            'bar-reviewer': 403, 'bar-editor': 403, 'anonymous': 401,
        },
        'https://bar.com/terms/options/bar-optionset': {
            'user': 403, 'reviewer': 403, 'editor': 201,
            'example-reviewer': 403, 'example-editor': 403, 'foo-user': 403,
            'foo-reviewer': 403, 'foo-editor': 403, 'bar-user': 403,
            'bar-reviewer': 403, 'bar-editor': 403, 'anonymous': 401,
        },
    },
    'update': {
        'https://foo.com/terms/options/foo-option-1': {
            'user': 404, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 403, 'foo-editor': 200, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://foo.com/terms/options/foo-option-2': {
            'user': 404, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 403, 'foo-editor': 200, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://bar.com/terms/options/bar-option-1': {
            'user': 404, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 403, 'bar-editor': 200, 'anonymous': 401,
        },
        'https://bar.com/terms/options/bar-option-2': {
            'user': 404, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 403, 'bar-editor': 200, 'anonymous': 401,
        },
    },
    'delete': {
        'https://foo.com/terms/options/foo-option-1': {
            'user': 404, 'reviewer': 403, 'editor': 204,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 403, 'foo-editor': 204, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://foo.com/terms/options/foo-option-2': {
            'user': 404, 'reviewer': 403, 'editor': 204,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 403, 'foo-editor': 204, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://bar.com/terms/options/bar-option-1': {
            'user': 404, 'reviewer': 403, 'editor': 204,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 403, 'bar-editor': 204, 'anonymous': 401,
        },
        'https://bar.com/terms/options/bar-option-2': {
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
        assert response.status_code == (
            STATUS_CODES['detail'].get(instance.uri, status_map['detail'])[username]
        ), response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Option.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': f'{instance.uri_path}_new_{username}',
            'comment': instance.comment,
            'text_en': instance.text_lang1,
            'text_de': instance.text_lang2
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_optionset(db, client, username, password):
    client.login(username=username, password=password)
    instances = Option.objects.all()

    for instance in instances:
        optionset = instance.optionsets.first()
        if optionset is not None:
            optionset_options = list(optionset.optionset_options.values_list('option', 'order'))
            order = optionset.optionset_options.aggregate(order=Max('order')).get('order') + 1

            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'uri_path': f'{instance.uri_path}_new_{username}',
                'comment': instance.comment,
                'text_en': instance.text_lang1,
                'text_de': instance.text_lang2,
                'optionsets': [optionset.id]
            }
            response = client.post(url, data, content_type='application/json')
            assert response.status_code == (
                STATUS_CODES['create-with-parent'].get(
                    optionset.uri, status_map['create-with-parent']
                )[username]
            ), response.json()

            if response.status_code == 201:
                new_instance = Option.objects.get(id=response.json().get('id'))
                optionset.refresh_from_db()
                assert [*optionset_options, (new_instance.id, order)] == \
                    list(optionset.optionset_options.values_list('option', 'order'))


def test_create_optionset_rejects_foreign_site_parent(db, client, sites):
    sites.activate('bar.com')
    client.login(username='bar-editor', password='bar-editor')

    instance = Option.objects.get(uri_path='foo-option-1')
    optionset = OptionSet.objects.get(uri_path='foo-optionset')

    optionset_options = list(optionset.optionset_options.values_list('option', 'order'))

    url = reverse(urlnames['list'])
    data = {
        'uri_prefix': 'https://bar.com/terms',
        'uri_path': f'{instance.uri_path}-bar-parent-denied',
        'comment': instance.comment,
        'text_en': instance.text_lang1,
        'text_de': instance.text_lang2,
        'optionsets': [optionset.id]
    }

    response = client.post(url, data, content_type='application/json')

    assert response.status_code == (
        STATUS_CODES['create-with-parent'].get(
            optionset.uri, status_map['create-with-parent']
        )['bar-editor']
    ), response.json()

    optionset.refresh_from_db()
    assert optionset_options == list(optionset.optionset_options.values_list('option', 'order'))


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
        assert response.status_code == (
            STATUS_CODES['update'].get(instance.uri, status_map['update'])[username]
        ), response.json()

        instance.refresh_from_db()
        assert optionsets == [optionset.id for optionset in instance.optionsets.all()]


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Option.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == (
            STATUS_CODES['delete'].get(instance.uri, status_map['delete'])[username]
        ), response.json()

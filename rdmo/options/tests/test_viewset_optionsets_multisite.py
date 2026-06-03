import xml.etree.ElementTree as et

import pytest

from django.urls import reverse

from rdmo.core.tests.constants import multisite_status_map as status_map
from rdmo.core.tests.constants import multisite_users as users

from ..models import OptionSet
from .test_viewset_optionsets import urlnames

STATUS_CODES = {
    'detail': {
        'https://foo.com/terms/options/foo-optionset': {
            'user': 404, 'reviewer': 200, 'editor': 200,
            'example-reviewer': 200, 'example-editor': 200, 'foo-user': 404,
            'foo-reviewer': 200, 'foo-editor': 200, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://bar.com/terms/options/bar-optionset': {
            'user': 404, 'reviewer': 200, 'editor': 200,
            'example-reviewer': 200, 'example-editor': 200, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 200, 'bar-editor': 200, 'anonymous': 401,
        },
    },
    'nested': {
        'https://foo.com/terms/options/foo-optionset': {
            'user': 404, 'reviewer': 200, 'editor': 200,
            'example-reviewer': 200, 'example-editor': 200, 'foo-user': 404,
            'foo-reviewer': 200, 'foo-editor': 200, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://bar.com/terms/options/bar-optionset': {
            'user': 404, 'reviewer': 200, 'editor': 200,
            'example-reviewer': 200, 'example-editor': 200, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 200, 'bar-editor': 200, 'anonymous': 401,
        },
    },
    'update': {
        'https://foo.com/terms/options/foo-optionset': {
            'user': 404, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 403, 'foo-editor': 200, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://bar.com/terms/options/bar-optionset': {
            'user': 404, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 403, 'bar-editor': 200, 'anonymous': 401,
        },
    },
    'delete': {
        'https://foo.com/terms/options/foo-optionset': {
            'user': 404, 'reviewer': 403, 'editor': 204,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 403, 'foo-editor': 204, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://bar.com/terms/options/bar-optionset': {
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
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == (
            STATUS_CODES['detail'].get(instance.uri, status_map['detail'])[username]
        ), response.json()


@pytest.mark.parametrize('username,password', users)
def test_nested(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['nested'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == (
            STATUS_CODES['nested'].get(instance.uri, status_map['nested'])[username]
        ), response.json()


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
            'uri_path': f'{instance.uri_path}_new_{username}',
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
        assert response.status_code == (
            STATUS_CODES['update'].get(instance.uri, status_map['update'])[username]
        ), response.json()

        if response.status_code == 200:
            instance.refresh_from_db()
            assert optionset_options == [{
                'option': optionset_option.option.id,
                'order': optionset_option.order
            } for optionset_option in instance.optionset_options.all()]
            assert conditions == [condition.pk for condition in instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == (
            STATUS_CODES['delete'].get(instance.uri, status_map['delete'])[username]
        ), response.json()


@pytest.mark.parametrize('username,password', users)
def test_detail_export(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

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
                assert child.tag in ['optionset', 'option']

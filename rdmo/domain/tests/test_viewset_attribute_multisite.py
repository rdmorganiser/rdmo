import xml.etree.ElementTree as et

import pytest

from django.urls import reverse

from ...core.tests import get_obj_perms_status_code
from ...core.tests import multisite_status_map as status_map
from ...core.tests import multisite_users as users
from ..models import Attribute
from .test_viewset_attribute import urlnames


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
        assert response.status_code == status_map['detail'][username], response.json()


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
        assert response.status_code == status_map['detail'][username], response.json()


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
def test_update_multisite(db, client, username, password):
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

        assert response.status_code == get_obj_perms_status_code(instance, username, 'update'), response.json()


@pytest.mark.parametrize('username,password', users)
def test_delete_multisite(db, client, username, password):
    client.login(username=username, password=password)
    instances = Attribute.objects.order_by('-level')

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == get_obj_perms_status_code(instance,username,'delete'), response.json()


@pytest.mark.parametrize('username,password', users)
def test_detail_export(db, client, username, password):
    client.login(username=username, password=password)
    instances = Attribute.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail_export'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.content

        if response.status_code == 200:
            root = et.fromstring(response.content)
            assert root.tag == 'rdmo'
            for child in root:
                assert child.tag in ['attribute']

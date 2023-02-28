import xml.etree.ElementTree as et

import pytest
from django.urls import reverse

from ..models import Catalog

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
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 401
    },
    'create': {
        'editor': 201, 'reviewer': 403, 'api': 201, 'user': 403, 'anonymous': 401
    },
    'update': {
        'editor': 200, 'reviewer': 403, 'api': 200, 'user': 403, 'anonymous': 401
    },
    'delete': {
        'editor': 204, 'reviewer': 403, 'api': 204, 'user': 403, 'anonymous': 401
    }
}

urlnames = {
    'list': 'v1-questions:catalog-list',
    'nested': 'v1-questions:catalog-nested',
    'index': 'v1-questions:catalog-index',
    'export': 'v1-questions:catalog-export',
    'detail': 'v1-questions:catalog-detail',
    'detail_export': 'v1-questions:catalog-detail-export',
    'copy': 'v1-questions:catalog-copy'
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
            assert child.tag in ['catalog', 'section', 'page', 'questionset', 'question']


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
            'uri_path': '%s_new_%s' % (instance.uri_path, username),
            'comment': instance.comment,
            'order': instance.order,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_m2m(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        catalog_sections = [{
            'section': section.section.id,
            'order': section.order
        } for section in instance.catalog_sections.all()[:1]]

        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': '%s_new_%s' % (instance.uri_path, username),
            'comment': instance.comment,
            'order': instance.order,
            'sections': catalog_sections,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()

        if response.status_code == 201:
            new_instance = Catalog.objects.get(id=response.json().get('id'))
            assert catalog_sections == [{
                'section': catalogsection.section_id,
                'order': catalogsection.order
            } for catalogsection in new_instance.catalog_sections.all()]


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        sections = [section.id for section in instance.sections.all()]

        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'order': instance.order,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()

        instance.refresh_from_db()
        assert sections == [section.id for section in instance.sections.all()]


@pytest.mark.parametrize('username,password', users)
def test_update_m2m(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        catalog_sections = [{
            'section': section.section.id,
            'order': section.order
        } for section in instance.catalog_sections.all()[:1]]

        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'order': instance.order,
            'sections': catalog_sections,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()

        if response.status_code == 200:
            instance.refresh_from_db()
            assert catalog_sections == [{
                'section': catalogsection.section_id,
                'order': catalogsection.order
            } for catalogsection in instance.catalog_sections.all()]


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_detail_export(db, client, username, password):
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
                assert child.tag in ['catalog', 'section', 'page', 'questionset', 'question']


@pytest.mark.parametrize('username,password', users)
def test_copy(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        url = reverse(urlnames['copy'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix + '-',
            'uri_path': instance.uri_path + '-',
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_copy_wrong(db, client, username, password):
    client.login(username=username, password=password)
    instance = Catalog.objects.first()

    url = reverse(urlnames['copy'], args=[instance.pk])
    data = {
        'uri_prefix': instance.uri_prefix,
        'uri_path': instance.uri_path
    }
    response = client.put(url, data, content_type='application/json')

    if status_map['create'][username] == 201:
        assert response.status_code == 400, response.json()
    else:
        assert response.status_code == status_map['create'][username], response.json()

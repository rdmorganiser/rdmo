import xml.etree.ElementTree as et

import pytest

from django.db.models import Max
from django.urls import reverse

from ..models import Section

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
    'nested': {
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
    'list': 'v1-questions:section-list',
    'nested': 'v1-questions:section-nested',
    'index': 'v1-questions:section-index',
    'export': 'v1-questions:section-export',
    'detail': 'v1-questions:section-detail',
    'detail_export': 'v1-questions:section-detail-export',
    'copy': 'v1-questions:section-copy'
}

export_formats = ('xml', 'rtf', 'odt', 'docx', 'html', 'markdown', 'tex', 'pdf')


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
            assert child.tag in ['section', 'page', 'questionset', 'question']


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Section.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_nested(db, client, username, password):
    client.login(username=username, password=password)
    instances = Section.objects.all()

    for instance in instances:
        url = reverse(urlnames['nested'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['nested'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Section.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': f'{instance.uri_path}_new_{username}',
            'comment': instance.comment,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_catalog(db, client, username, password):
    client.login(username=username, password=password)
    instances = Section.objects.all()

    for instance in instances:
        catalog = instance.catalogs.first()
        if catalog is not None:
            catalog_sections = list(catalog.catalog_sections.values_list('section', 'order'))
            order = catalog.catalog_sections.aggregate(order=Max('order')).get('order') + 1

            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'uri_path': f'{instance.uri_path}_new_{username}',
                'comment': instance.comment,
                'title_en': instance.title_lang1,
                'title_de': instance.title_lang2,
                'catalogs': [catalog.id]
            }
            response = client.post(url, data, content_type='application/json')
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = Section.objects.get(id=response.json().get('id'))
                catalog.refresh_from_db()
                assert [*catalog_sections, (new_instance.id, order)] == \
                    list(catalog.catalog_sections.values_list('section', 'order'))


@pytest.mark.parametrize('username,password', users)
def test_create_m2m(db, client, username, password):
    client.login(username=username, password=password)
    instances = Section.objects.all()

    for instance in instances:
        section_pages = [{
            'page': section_page.page_id,
            'order': section_page.order
        } for section_page in instance.section_pages.all()[:1]]

        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': f'{instance.uri_path}_new_{username}',
            'comment': instance.comment,
            'pages': section_pages,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2
        }

        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()

        if response.status_code == 201:
            new_instance = Section.objects.get(id=response.json().get('id'))
            assert section_pages == [{
                'page': section_page.page_id,
                'order': section_page.order
            } for section_page in new_instance.section_pages.all()]


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Section.objects.all()

    for instance in instances:
        catalogs = [catalog.id for catalog in instance.catalogs.all()]
        pages = [page.id for page in instance.pages.all()]

        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()

        instance.refresh_from_db()
        assert catalogs == [catalog.id for catalog in instance.catalogs.all()]
        assert pages == [page.id for page in instance.pages.all()]


@pytest.mark.parametrize('username,password', users)
def test_update_m2m(db, client, username, password):
    client.login(username=username, password=password)
    instances = Section.objects.all()

    for instance in instances:
        pages = [{
            'page': section_page.page_id,
            'order': section_page.order
        } for section_page in instance.section_pages.all()[:1]]

        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'pages': pages,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()

        if response.status_code == 200:
            instance.refresh_from_db()
            assert pages == [{
                'page': section_page.page_id,
                'order': section_page.order
            } for section_page in instance.section_pages.all()]


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Section.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_detail_export(db, client, username, password, export_format):
    client.login(username=username, password=password)
    instance = Section.objects.first()

    url = reverse(urlnames['detail_export'], args=[instance.pk]) + export_format + '/'
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content

    if response.status_code == 200 and export_format == 'xml':
        root = et.fromstring(response.content)
        assert root.tag == 'rdmo'
        for child in root:
            assert child.tag in ['section', 'page', 'questionset', 'question']

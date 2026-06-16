import xml.etree.ElementTree as et

import pytest

from django.contrib.sites.models import Site
from django.urls import reverse

from rdmo.core.tests.constants import multisite_status_map as status_map
from rdmo.core.tests.constants import multisite_users as users

from ..models import Catalog
from .test_viewset_catalog import export_formats, urlnames

STATUS_CODES = {
    'detail': {
        'https://foo.com/terms/questions/foo-catalog': {
            'user': 404, 'reviewer': 200, 'editor': 200,
            'example-reviewer': 200, 'example-editor': 200, 'foo-user': 404,
            'foo-reviewer': 200, 'foo-editor': 200, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://bar.com/terms/questions/bar-catalog': {
            'user': 404, 'reviewer': 200, 'editor': 200,
            'example-reviewer': 200, 'example-editor': 200, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 200, 'bar-editor': 200, 'anonymous': 401,
        },
    },
    'update': {
        'https://foo.com/terms/questions/foo-catalog': {
            'user': 404, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 403, 'foo-editor': 200, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://bar.com/terms/questions/bar-catalog': {
            'user': 404, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 403, 'bar-editor': 200, 'anonymous': 401,
        },
    },
    'delete': {
        'https://foo.com/terms/questions/foo-catalog': {
            'user': 404, 'reviewer': 403, 'editor': 204,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 403, 'foo-editor': 204, 'bar-user': 404,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'https://bar.com/terms/questions/bar-catalog': {
            'user': 404, 'reviewer': 403, 'editor': 204,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 404,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 404,
            'bar-reviewer': 403, 'bar-editor': 204, 'anonymous': 401,
        },
    },
    'toggle-site': {
        'https://foo.com/terms/questions/foo-catalog': {
            'user': 403, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 403, 'example-editor': 200, 'foo-user': 403,
            'foo-reviewer': 403, 'foo-editor': 403, 'bar-user': 403,
            'bar-reviewer': 403, 'bar-editor': 403, 'anonymous': 401,
        },
        'https://bar.com/terms/questions/bar-catalog': {
            'user': 403, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 403, 'example-editor': 200, 'foo-user': 403,
            'foo-reviewer': 403, 'foo-editor': 403, 'bar-user': 403,
            'bar-reviewer': 403, 'bar-editor': 403, 'anonymous': 401,
        },
    },
}


urlnames['catalog-toggle-site'] = 'v1-questions:catalog-toggle-site'




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
            assert child.tag in ['catalog', 'section', 'page', 'questionset', 'question']


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == (
            STATUS_CODES['detail'].get(instance.uri, status_map['detail'])[username]
        ), response.json()


@pytest.mark.parametrize('username,password', users)
def test_nested(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        url = reverse(urlnames['nested'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == (
            STATUS_CODES['detail'].get(instance.uri, status_map['detail'])[username]
        ), response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': f'{instance.uri_path}_new_{username}',
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
            'uri_path': f'{instance.uri_path}_new_{username}',
            'comment': instance.comment,
            'order': instance.order,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'sections': catalog_sections
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()

        if response.status_code == 201:
            new_instance = Catalog.objects.get(id=response.json().get('id'))
            assert catalog_sections == [{
                'section': section.section.id,
                'order': section.order
            } for section in new_instance.catalog_sections.all()]


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        catalog_sections = [{
            'section': section.section.id,
            'order': section.order
        } for section in instance.catalog_sections.all()]

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
        assert response.status_code == (
            STATUS_CODES['update'].get(instance.uri, status_map['update'])[username]
        ), response.json()

        instance.refresh_from_db()
        assert catalog_sections == [{
            'section': section.section.id,
            'order': section.order
        } for section in instance.catalog_sections.all()]


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
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'sections': catalog_sections
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == (
            STATUS_CODES['update'].get(instance.uri, status_map['update'])[username]
        ), response.json()

        if response.status_code == 200:
            instance.refresh_from_db()
            assert catalog_sections == [{
                'section': section.section.id,
                'order': section.order
            } for section in instance.catalog_sections.all()]


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == (
            STATUS_CODES['delete'].get(instance.uri, status_map['delete'])[username]
        ), response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_detail_export(db, client, username, password, export_format):
    client.login(username=username, password=password)
    instance = Catalog.objects.first()

    url = reverse(urlnames['detail_export'], args=[instance.pk]) + export_format + '/'
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content

    if response.status_code == 200 and export_format == 'xml':
        root = et.fromstring(response.content)
        assert root.tag == 'rdmo'
        for child in root:
            assert child.tag in ['catalog', 'section', 'page', 'questionset', 'question']


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('add_or_remove,has_current_site_check', [('add', True), ('remove', False)])
@pytest.mark.parametrize('locked', [True, False])
def test_update_catalog_toggle_site(db, client, username, password, add_or_remove, has_current_site_check, locked):
    client.login(username=username, password=password)
    instances = Catalog.objects.all()
    current_site = Site.objects.get_current()

    for instance in instances:
        if add_or_remove == 'add':
            instance.sites.remove(current_site)
        elif add_or_remove == 'remove':
            instance.sites.add(current_site)

        # locked state should not affect this toggle
        instance.locked = locked
        instance.save()

        before_put_has_current_site = instance.sites.filter(id=current_site.id).exists()

        url = reverse(urlnames['catalog-toggle-site'], kwargs={'pk': instance.pk})

        response = client.put(url, {}, content_type='application/json')
        assert response.status_code == (
            STATUS_CODES['toggle-site'].get(instance.uri, status_map['toggle-site'])[username]
        ), response.json()
        instance.refresh_from_db()
        after_put_has_current_site = instance.sites.filter(id=current_site.id).exists()
        if response.status_code == 200:
            # check if instance now has the current site or not
            assert after_put_has_current_site is has_current_site_check
        else:
            # check that the instance was not updated
            assert after_put_has_current_site is before_put_has_current_site

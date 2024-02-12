import xml.etree.ElementTree as et

import pytest

from django.contrib.sites.models import Site
from django.urls import reverse

from ...core.tests import get_obj_perms_status_code
from ...core.tests import multisite_status_map as status_map
from ...core.tests import multisite_users as users
from ..models import Task
from .test_viewset_task import export_formats, urlnames

urlnames['task-add-site'] = 'v1-tasks:task-add-site'
urlnames['task-remove-site'] = 'v1-tasks:task-remove-site'


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
            assert child.tag in ['task']


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Task.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Task.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': f'{instance.uri_path}_new_{username}',
            'comment': instance.comment,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'text_en': instance.text_lang1,
            'text_de': instance.text_lang2,
            'start_attribute': instance.start_attribute.pk if instance.start_attribute else '',
            'end_attribute': instance.end_attribute.pk if instance.end_attribute else '',
            'days_before': instance.days_before or 0,
            'days_after': instance.days_after or 0,
            'conditions': [condition.pk for condition in instance.conditions.all()]
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Task.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'text_en': instance.text_lang1,
            'text_de': instance.text_lang2,
            'start_attribute': instance.start_attribute.pk if instance.start_attribute else '',
            'end_attribute': instance.end_attribute.pk if instance.end_attribute else '',
            'days_before': instance.days_before,
            'days_after': instance.days_after,
            'conditions': [condition.pk for condition in instance.conditions.all()]
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == get_obj_perms_status_code(instance, username, 'update'), response.json()


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Task.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == get_obj_perms_status_code(instance, username, 'delete'), response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_detail_export(db, client, username, password, export_format):
    client.login(username=username, password=password)
    instance = Task.objects.first()

    url = reverse(urlnames['detail_export'], args=[instance.pk]) + export_format + '/'
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content

    if response.status_code == 200 and export_format == 'xml':
        root = et.fromstring(response.content)
        assert root.tag == 'rdmo'
        for child in root:
            assert child.tag in ['task']



@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('add_or_remove, has_current_site_check', [('add', True), ('remove', False)])
def test_update_task_toggle_site(db, client, username, password, add_or_remove, has_current_site_check):
    client.login(username=username, password=password)
    instances = Task.objects.all()
    current_site = Site.objects.get_current()

    for instance in instances:
        before_has_current_site = instance.sites.filter(id=current_site.id).exists()

        url = reverse(urlnames[f'task-{add_or_remove}-site'], kwargs={'pk': instance.pk})

        response = client.put(url, {}, content_type='application/json')
        assert response.status_code == get_obj_perms_status_code(instance, username, 'toggle-site'), response.json()
        instance.refresh_from_db()
        after_has_current_site = instance.sites.filter(id=current_site.id).exists()
        if response.status_code == 200:
            # check if instance now has the current site or not
            assert after_has_current_site is has_current_site_check
        else:
            # check that the instance was not updated
            assert after_has_current_site is before_has_current_site

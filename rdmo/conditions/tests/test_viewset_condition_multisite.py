import xml.etree.ElementTree as et

import pytest

from django.urls import reverse

from rdmo.core.tests.constants import multisite_status_map as status_map
from rdmo.core.tests.constants import multisite_users as users
from rdmo.core.tests.utils import get_obj_perms_status_code

from ..models import Condition
from .test_viewset_condition import export_formats, urlnames


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
            'uri_path': f'{instance.uri_path}_new_{username}',
            'comment': instance.comment,
            'source': instance.source.pk,
            'relation': instance.relation,
            'target_text': instance.target_text,
            'target_option': instance.target_option.pk if instance.target_option else ''
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_optionset(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        optionset = instance.optionsets.first()
        if optionset:
            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'uri_path': f'{instance.uri_path}_new_{username}',
                'comment': instance.comment,
                'source': instance.source.pk,
                'relation': instance.relation,
                'target_text': instance.target_text,
                'target_option': instance.target_option.pk if instance.target_option else '',
                'optionsets': [optionset.id]
            }
            response = client.post(url, data)
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = Condition.objects.get(id=response.json().get('id'))
                assert [optionset.id] == [optionset.id for optionset in new_instance.optionsets.all()]


@pytest.mark.parametrize('username,password', users)
def test_create_page(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        page = instance.pages.first()
        if page:
            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'uri_path': f'{instance.uri_path}_new_{username}',
                'comment': instance.comment,
                'source': instance.source.pk,
                'relation': instance.relation,
                'target_text': instance.target_text,
                'target_option': instance.target_option.pk if instance.target_option else '',
                'pages': [page.id]
            }
            response = client.post(url, data)
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = Condition.objects.get(id=response.json().get('id'))
                assert [page.id] == [page.id for page in new_instance.pages.all()]


@pytest.mark.parametrize('username,password', users)
def test_create_questionset(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        questionset = instance.questionsets.first()
        if questionset:
            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'uri_path': f'{instance.uri_path}_new_{username}',
                'comment': instance.comment,
                'source': instance.source.pk,
                'relation': instance.relation,
                'target_text': instance.target_text,
                'target_option': instance.target_option.pk if instance.target_option else '',
                'questionsets': [questionset.id]
            }
            response = client.post(url, data)
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = Condition.objects.get(id=response.json().get('id'))
                assert [questionset.id] == [questionset.id for questionset in new_instance.questionsets.all()]


@pytest.mark.parametrize('username,password', users)
def test_create_question(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        question = instance.questions.first()
        if question:
            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'uri_path': f'{instance.uri_path}_new_{username}',
                'comment': instance.comment,
                'source': instance.source.pk,
                'relation': instance.relation,
                'target_text': instance.target_text,
                'target_option': instance.target_option.pk if instance.target_option else '',
                'questions': [question.id]
            }
            response = client.post(url, data)
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = Condition.objects.get(id=response.json().get('id'))
                assert [question.id] == [question.id for question in new_instance.questions.all()]


@pytest.mark.parametrize('username,password', users)
def test_create_task(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        task = instance.tasks.first()
        if task:
            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'uri_path': f'{instance.uri_path}_new_{username}',
                'comment': instance.comment,
                'source': instance.source.pk,
                'relation': instance.relation,
                'target_text': instance.target_text,
                'target_option': instance.target_option.pk if instance.target_option else '',
                'tasks': [task.id]
            }
            response = client.post(url, data)
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = Condition.objects.get(id=response.json().get('id'))
                assert [task.id] == [task.id for task in new_instance.tasks.all()]


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'source': instance.source.pk,
            'relation': instance.relation,
            'target_text': instance.target_text,
            'target_option': instance.target_option.pk if instance.target_option else None
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == get_obj_perms_status_code(instance, username, 'update'), response.json()


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == get_obj_perms_status_code(instance, username, 'delete'), response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_detail_export(db, client, username, password, export_format):
    client.login(username=username, password=password)
    instance = Condition.objects.first()

    url = reverse(urlnames['detail_export'], args=[instance.pk]) + export_format + '/'
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content

    if response.status_code == 200 and export_format == 'xml':
        root = et.fromstring(response.content)
        assert root.tag == 'rdmo'
        for child in root:
            assert child.tag in ['condition']

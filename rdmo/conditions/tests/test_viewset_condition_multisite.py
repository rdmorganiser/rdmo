import xml.etree.ElementTree as et

import pytest
from django.urls import reverse
from django.contrib.sites.models import Site

from ..models import Condition

from .test_viewset_condition import export_formats

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
    'copy': {
        'foo-user': 404, 'foo-reviewer': 403, 'foo-editor': 201,
        'bar-user': 404, 'bar-reviewer': 403, 'bar-editor': 201,
        'user': 404, 'example-reviewer': 403, 'example-editor': 201,
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


status_map_object_permissions = {
    'copy': {
        'foo-condition': {
            'foo-reviewer': 403, 'foo-editor': 201,
            'bar-reviewer': 404, 'bar-editor': 404,
            'example-reviewer': 404, 'example-editor': 404,
        },
        'bar-condition': {
            'foo-reviewer': 404, 'foo-editor': 404,
            'bar-reviewer': 403, 'bar-editor': 201,
            'example-reviewer': 404, 'example-editor': 404,
        }
    },
    'update': {
        'foo-condition': {
            'foo-reviewer': 403, 'foo-editor': 200,
            'bar-reviewer': 404, 'bar-editor': 404,
            'example-reviewer': 404, 'example-editor': 404,
        },
        'bar-condition': {
            'foo-reviewer': 404, 'foo-editor': 404,
            'bar-reviewer': 403, 'bar-editor': 200,
            'example-reviewer': 404, 'example-editor': 404,
        }
    },
    'delete': {
        'foo-condition': {
            'foo-reviewer': 403, 'foo-editor': 204,
            'bar-reviewer': 404, 'bar-editor': 404,
            'example-reviewer': 404, 'example-editor': 404,
        },
        'bar-condition': {
            'foo-reviewer': 404, 'foo-editor': 404,
            'bar-reviewer': 403, 'bar-editor': 204,
            'example-reviewer': 404, 'example-editor': 404,
        }
    },
}

def get_status_map_or_obj_perms(instance, username, method):
    ''' looks for the object permissions of the instance and returns the status code '''
    if instance.editors.exists():
        try:
            return status_map_object_permissions[method][instance.key][username]
        except KeyError:
            return status_map[method][username]
    else:
        return status_map[method][username]


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
def test_create_optionset(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        optionset = instance.optionsets.first()
        if optionset:
            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'key': '%s_new_%s' % (instance.key, username),
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
                'key': '%s_new_%s' % (instance.key, username),
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
                'key': '%s_new_%s' % (instance.key, username),
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
                'key': '%s_new_%s' % (instance.key, username),
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
                'key': '%s_new_%s' % (instance.key, username),
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
            'key': instance.key,
            'comment': instance.comment,
            'source': instance.source.pk,
            'relation': instance.relation,
            'target_text': instance.target_text,
            'target_option': instance.target_option.pk if instance.target_option else None
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == get_status_map_or_obj_perms(instance, username, 'update'), response.json()


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == get_status_map_or_obj_perms(instance, username, 'delete'), response.json()


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


@pytest.mark.parametrize('username,password', users)
def test_copy(db, client, username, password):
    client.login(username=username, password=password)
    instances = Condition.objects.all()

    for instance in instances:
        url = reverse(urlnames['copy'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix + '-',
            'key': instance.key + '-'
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == get_status_map_or_obj_perms(instance, username, 'copy'), response.json()


@pytest.mark.parametrize('username,password', users)
def test_copy_wrong(db, client, username, password):
    client.login(username=username, password=password)
    instance = Condition.objects.first()

    url = reverse(urlnames['copy'], args=[instance.pk])
    data = {
        'uri_prefix': instance.uri_prefix,
        'key': instance.key
    }
    response = client.put(url, data, content_type='application/json')

    if status_map['copy'][username] == 201:
        assert response.status_code == 400, response.json()
    else:
        assert response.status_code == get_status_map_or_obj_perms(instance, username, 'copy'), response.json()

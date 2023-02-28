import xml.etree.ElementTree as et

import pytest
from django.urls import reverse

from ..models import Question

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
    'list': 'v1-questions:question-list',
    'nested': 'v1-questions:question-nested',
    'index': 'v1-questions:question-index',
    'export': 'v1-questions:question-export',
    'detail': 'v1-questions:question-detail',
    'detail_export': 'v1-questions:question-detail-export',
    'copy': 'v1-questions:question-copy'
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
            assert child.tag in ['question']


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Question.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_nested(db, client, username, password):
    client.login(username=username, password=password)
    instances = Question.objects.all()

    for instance in instances:
        url = reverse(urlnames['nested'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Question.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': '%s_new_%s' % (instance.uri_path, username),
            'comment': instance.comment or '',
            'attribute': instance.attribute.pk if instance.attribute else '',
            'page': instance.page.pk if instance.page else '',
            'questionset': instance.questionset.pk if instance.questionset else '',
            'is_collection': instance.is_collection,
            'order': instance.order,
            'help_en': instance.help_lang1 or '',
            'help_de': instance.help_lang2 or '',
            'text_en': instance.text_lang1 or '',
            'text_de': instance.text_lang2 or '',
            'verbose_name_en': instance.verbose_name_lang1 or '',
            'verbose_name_de': instance.verbose_name_lang2 or '',
            'verbose_name_plural_en': instance.verbose_name_plural_lang1 or '',
            'verbose_name_plural_de': instance.verbose_name_plural_lang2 or '',
            'widget_type': instance.widget_type,
            'value_type': instance.value_type,
            'minimum': instance.minimum or '',
            'maximum': instance.maximum or '',
            'step': instance.step or '',
            'unit': instance.unit or '',
            'optionsets': [optionset.pk for optionset in instance.optionsets.all()],
            'conditions': [condition.pk for condition in instance.conditions.all()]
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Question.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'attribute': instance.attribute.pk if instance.attribute else None,
            'page': instance.page.pk if instance.page else None,
            'questionset': instance.questionset.pk if instance.questionset else None,
            'is_collection': instance.is_collection,
            'order': instance.order,
            'help_en': instance.help_lang1,
            'help_de': instance.help_lang2,
            'text_en': instance.text_lang1,
            'text_de': instance.text_lang2,
            'verbose_name_en': instance.verbose_name_lang1,
            'verbose_name_de': instance.verbose_name_lang2,
            'verbose_name_plural_en': instance.verbose_name_plural_lang1,
            'verbose_name_plural_de': instance.verbose_name_plural_lang2,
            'widget_type': instance.widget_type,
            'value_type': instance.value_type,
            'minimum': instance.minimum,
            'maximum': instance.maximum,
            'step': instance.step,
            'unit': instance.unit,
            'optionsets': [optionset.pk for optionset in instance.optionsets.all()],
            'conditions': [condition.pk for condition in instance.conditions.all()],
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Question.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_detail_export(db, client, username, password):
    client.login(username=username, password=password)
    instances = Question.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail_export'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['list'][username], response.content

        if response.status_code == 200:
            root = et.fromstring(response.content)
            assert root.tag == 'rdmo'
            for child in root:
                assert child.tag in ['question']


@pytest.mark.parametrize('username,password', users)
def test_copy(db, client, username, password):
    client.login(username=username, password=password)
    instances = Question.objects.all()

    for instance in instances:
        url = reverse(urlnames['copy'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix + '-',
            'uri_path': instance.uri_path + '-',
            'page': instance.page.pk if instance.page else None,
            'questionset': instance.questionset.pk if instance.questionset else None
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_copy_wrong(db, client, username, password):
    client.login(username=username, password=password)
    instance = Question.objects.first()

    url = reverse(urlnames['copy'], args=[instance.pk])
    data = {
        'uri_prefix': instance.uri_prefix,
        'uri_path': instance.uri_path,
        'page': instance.page.pk if instance.page else None,
        'questionset': instance.questionset.pk if instance.questionset else None
    }
    response = client.put(url, data, content_type='application/json')

    if status_map['create'][username] == 201:
        assert response.status_code == 400, response.json()
    else:
        assert response.status_code == status_map['create'][username], response.json()

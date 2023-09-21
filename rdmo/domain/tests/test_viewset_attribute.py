import xml.etree.ElementTree as et

import pytest

from django.urls import reverse

from ..models import Attribute

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
    'list': 'v1-domain:attribute-list',
    'nested': 'v1-domain:attribute-nested',
    'export': 'v1-domain:attribute-export',
    'detail': 'v1-domain:attribute-detail',
    'detail_export': 'v1-domain:attribute-detail-export',
    'copy': 'v1-domain:attribute-copy'
}

export_formats = ('xml', 'csvcomma', 'csvsemicolon', 'rtf', 'odt', 'docx', 'html', 'markdown', 'tex', 'pdf')


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
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
            assert child.tag in ['attribute']


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Attribute.objects.order_by('-level')

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_nested(db, client, username, password):
    client.login(username=username, password=password)
    instances = Attribute.objects.order_by('-level')

    for instance in instances:
        url = reverse(urlnames['nested'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
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
def test_create_condition(db, client, username, password):
    client.login(username=username, password=password)
    instances = Attribute.objects.order_by('-level')

    for instance in instances:
        condition = instance.conditions.first()
        if condition:
            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'key': f'{instance.key}_new_{username}',
                'comment': '',
                'parent': instance.parent.pk if instance.parent else '',
                'conditions': [condition.id]
            }
            response = client.post(url, data)
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = Attribute.objects.get(id=response.json().get('id'))
                assert [condition.id] == [condition.id for condition in new_instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_create_page(db, client, username, password):
    client.login(username=username, password=password)
    instances = Attribute.objects.order_by('-level')

    for instance in instances:
        page = instance.pages.first()
        if page:
            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'key': f'{instance.key}_new_{username}',
                'comment': '',
                'parent': instance.parent.pk if instance.parent else '',
                'pages': [page.id]
            }
            response = client.post(url, data)
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = Attribute.objects.get(id=response.json().get('id'))
                assert [page.id] == [page.id for page in new_instance.pages.all()]


@pytest.mark.parametrize('username,password', users)
def test_create_questionset(db, client, username, password):
    client.login(username=username, password=password)
    instances = Attribute.objects.order_by('-level')

    for instance in instances:
        questionset = instance.questionsets.first()
        if questionset:
            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'key': f'{instance.key}_new_{username}',
                'comment': '',
                'parent': instance.parent.pk if instance.parent else '',
                'questionsets': [questionset.id]
            }
            response = client.post(url, data)
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = Attribute.objects.get(id=response.json().get('id'))
                assert [questionset.id] == [questionset.id for questionset in new_instance.questionsets.all()]


@pytest.mark.parametrize('username,password', users)
def test_create_question(db, client, username, password):
    client.login(username=username, password=password)
    instances = Attribute.objects.order_by('-level')

    for instance in instances:
        question = instance.questions.first()
        if question:
            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'key': f'{instance.key}_new_{username}',
                'comment': '',
                'parent': instance.parent.pk if instance.parent else '',
                'questions': [question.id]
            }
            response = client.post(url, data)
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = Attribute.objects.get(id=response.json().get('id'))
                assert [question.id] == [question.id for question in new_instance.questions.all()]


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
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
        assert response.status_code == status_map['update'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Attribute.objects.order_by('-level')

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_detail_export(db, client, username, password, export_format):
    client.login(username=username, password=password)
    instance = Attribute.objects.first()

    url = reverse(urlnames['detail_export'], args=[instance.pk]) + export_format + '/'
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content

    if response.status_code == 200 and export_format == 'xml':
        root = et.fromstring(response.content)
        assert root.tag == 'rdmo'
        for child in root:
            assert child.tag in ['attribute']

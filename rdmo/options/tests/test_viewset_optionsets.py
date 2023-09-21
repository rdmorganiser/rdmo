import xml.etree.ElementTree as et

import pytest

from django.urls import reverse

from ..models import OptionSet

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
    'list': 'v1-options:optionset-list',
    'nested': 'v1-options:optionset-nested',
    'index': 'v1-options:optionset-index',
    'export': 'v1-options:optionset-export',
    'detail': 'v1-options:optionset-detail',
    'detail_export': 'v1-options:optionset-detail-export',
    'copy': 'v1-options:optionset-copy'
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
            assert child.tag in ['optionset', 'option']


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_nested(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['nested'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


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
            'order': instance.order
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_question(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        question = instance.questions.first()
        if question:
            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'uri_path': f'{instance.uri_path}_new_{username}',
                'comment': instance.comment,
                'order': instance.order,
                'questions': [question.id]
            }
            response = client.post(url, data, content_type='application/json')
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = OptionSet.objects.get(id=response.json().get('id'))
                assert [question.id] == [question.id for question in new_instance.questions.all()]


@pytest.mark.parametrize('username,password', users)
def test_create_m2m(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        optionset_options = [{
            'option': optionset_option.option.id,
            'order': optionset_option.order
        } for optionset_option in instance.optionset_options.all()[:1]]
        conditions = [condition.pk for condition in instance.conditions.all()[:1]]

        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': f'{instance.uri_path}_new_{username}',
            'comment': instance.comment,
            'order': instance.order,
            'options': optionset_options,
            'conditions': conditions,
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()

        if response.status_code == 201:
            new_instance = OptionSet.objects.get(id=response.json().get('id'))
            assert optionset_options == [{
                'option': optionset_option.option.id,
                'order': optionset_option.order
            } for optionset_option in new_instance.optionset_options.all()]
            assert conditions == [condition.pk for condition in new_instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        optionset_options = [{
            'option': optionset_option.option.id,
            'order': optionset_option.order
        } for optionset_option in instance.optionset_options.all()]
        conditions = [condition.pk for condition in instance.conditions.all()]

        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'order': instance.order,
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()

        instance.refresh_from_db()
        assert optionset_options == [{
            'option': optionset_option.option.id,
            'order': optionset_option.order
        } for optionset_option in instance.optionset_options.all()]
        assert conditions == [condition.pk for condition in instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_update_m2m(db, client, username, password):
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
        assert response.status_code == status_map['update'][username], response.json()

        if response.status_code == 200:
            instance.refresh_from_db()
            assert optionset_options == [{
                'option': optionset_option.option.id,
                'order': optionset_option.order
            } for optionset_option in instance.optionset_options.all()]
            assert conditions == [condition.pk for condition in instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_update_m2m_order(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        optionset_options = [{
            'option': optionset_option.option.id,
            'order': optionset_option.order
        } for optionset_option in instance.optionset_options.all().order_by('-order')]

        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'order': instance.order,
            'options': optionset_options
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()

        if response.status_code == 200:
            instance.refresh_from_db()
            assert optionset_options == [{
                'option': optionset_option.option.id,
                'order': optionset_option.order
            } for optionset_option in instance.optionset_options.all().order_by('-order')]


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = OptionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_detail_export(db, client, username, password, export_format):
    client.login(username=username, password=password)
    instance = OptionSet.objects.first()

    url = reverse(urlnames['detail_export'], args=[instance.pk]) + export_format + '/'
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content

    if response.status_code == 200 and export_format == 'xml':
        root = et.fromstring(response.content)
        assert root.tag == 'rdmo'
        for child in root:
            assert child.tag in ['optionset', 'option']

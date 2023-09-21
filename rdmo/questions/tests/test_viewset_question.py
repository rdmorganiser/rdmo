import xml.etree.ElementTree as et

import pytest

from django.db.models import Max
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
    'list': 'v1-questions:question-list',
    'index': 'v1-questions:question-index',
    'export': 'v1-questions:question-export',
    'detail': 'v1-questions:question-detail',
    'detail_export': 'v1-questions:question-detail-export',
    'copy': 'v1-questions:question-copy'
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
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Question.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': f'{instance.uri_path}_new_{username}',
            'comment': instance.comment or '',
            'attribute': instance.attribute.pk if instance.attribute else '',
            'is_collection': instance.is_collection,
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
            'unit': instance.unit or ''
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_page(db, client, username, password):
    client.login(username=username, password=password)
    instances = Question.objects.all()

    for instance in instances:
        page = instance.pages.first()
        if page is not None:
            page_questions = list(page.page_questions.values_list('question', 'order'))
            order = page.page_questions.aggregate(order=Max('order')).get('order') + 1

            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'uri_path': f'{instance.uri_path}_new_{username}',
                'comment': instance.comment or '',
                'attribute': instance.attribute.pk if instance.attribute else '',
                'is_collection': instance.is_collection,
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
                'pages': [page.id]
            }
            response = client.post(url, data, content_type='application/json')
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = Question.objects.get(id=response.json().get('id'))
                page.refresh_from_db()
                assert [*page_questions, (new_instance.id, order)] == \
                    list(page.page_questions.values_list('question', 'order'))


@pytest.mark.parametrize('username,password', users)
def test_create_questionset(db, client, username, password):
    client.login(username=username, password=password)
    instances = Question.objects.all()

    for instance in instances:
        questionset = instance.questionsets.first()
        if questionset is not None:
            questionset_questions = list(questionset.questionset_questions.values_list('question', 'order'))
            order = questionset.questionset_questions.aggregate(order=Max('order')).get('order') + 1

            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'uri_path': f'{instance.uri_path}_new_{username}',
                'comment': instance.comment or '',
                'attribute': instance.attribute.pk if instance.attribute else '',
                'is_collection': instance.is_collection,
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
                'questionsets': [questionset.id]
            }
            response = client.post(url, data, content_type='application/json')
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = Question.objects.get(id=response.json().get('id'))
                questionset.refresh_from_db()
                assert [*questionset_questions, (new_instance.id, order)] == \
                    list(questionset.questionset_questions.values_list('question', 'order'))


@pytest.mark.parametrize('username,password', users)
def test_create_m2m(db, client, username, password):
    client.login(username=username, password=password)
    instances = Question.objects.all()

    for instance in instances:
        optionsets = [optionset.id for optionset in instance.optionsets.all()[:1]]
        conditions = [condition.pk for condition in instance.conditions.all()[:1]]

        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': f'{instance.uri_path}_new_{username}',
            'comment': instance.comment or '',
            'attribute': instance.attribute.pk if instance.attribute else '',
            'is_collection': instance.is_collection,
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
            'optionsets': optionsets,
            'conditions': conditions
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()

        if response.status_code == 201:
            new_instance = Question.objects.get(id=response.json().get('id'))
            assert optionsets == [optionset.pk for optionset in new_instance.optionsets.all()]
            assert conditions == [condition.pk for condition in new_instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Question.objects.all()

    for instance in instances:
        pages = [page.id for page in instance.pages.all()]
        questionsets = [questionset.id for questionset in instance.questionsets.all()]
        optionsets = [optionset.id for optionset in instance.optionsets.all()]
        conditions = [condition.pk for condition in instance.conditions.all()]

        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'attribute': instance.attribute.pk if instance.attribute else None,
            'is_collection': instance.is_collection,
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

        instance.refresh_from_db()
        assert pages == [page.id for page in instance.pages.all()]
        assert questionsets == [questionset.id for questionset in instance.questionsets.all()]
        assert optionsets == [optionset.id for optionset in instance.optionsets.all()]
        assert conditions == [condition.pk for condition in instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_update_m2m(db, client, username, password):
    client.login(username=username, password=password)
    instances = Question.objects.all()

    for instance in instances:
        optionsets = [optionset.id for optionset in instance.optionsets.all()[:1]]
        conditions = [condition.pk for condition in instance.conditions.all()[:1]]

        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'attribute': instance.attribute.pk if instance.attribute else None,
            'is_collection': instance.is_collection,
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
            'optionsets': optionsets,
            'conditions': conditions
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()

        if response.status_code == 200:
            instance.refresh_from_db()
            assert optionsets == [optionset.pk for optionset in instance.optionsets.all()]
            assert conditions == [condition.pk for condition in instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Question.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_detail_export(db, client, username, password, export_format):
    client.login(username=username, password=password)
    instance = Question.objects.first()

    url = reverse(urlnames['detail_export'], args=[instance.pk]) + export_format + '/'
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content

    if response.status_code == 200 and export_format == 'xml':
        root = et.fromstring(response.content)
        assert root.tag == 'rdmo'
        for child in root:
            assert child.tag in ['question']

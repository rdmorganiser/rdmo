import xml.etree.ElementTree as et

import pytest
from django.urls import reverse

from ..models import QuestionSet

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
    'list': 'v1-questions:questionset-list',
    'nested': 'v1-questions:questionset-nested',
    'index': 'v1-questions:questionset-index',
    'export': 'v1-questions:questionset-export',
    'detail': 'v1-questions:questionset-detail',
    'detail_export': 'v1-questions:questionset-detail-export',
    'copy': 'v1-questions:questionset-copy'
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
            assert child.tag in ['questionset', 'question']


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_nested(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['nested'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': '%s_new_%s' % (instance.uri_path, username),
            'comment': instance.comment,
            'attribute': instance.attribute.pk if instance.attribute else '',
            'is_collection': instance.is_collection,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'help_en': instance.help_lang1,
            'help_de': instance.help_lang2,
            'verbose_name_en': instance.verbose_name_lang1,
            'verbose_name_de': instance.verbose_name_lang2,
            'verbose_name_plural_en': instance.verbose_name_plural_lang1,
            'verbose_name_plural_de': instance.verbose_name_plural_lang2
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_m2m(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.all()

    for instance in instances:
        questionsets = [{
            'questionset': questionset_questionset.questionset.id,
            'order': questionset_questionset.order
        } for questionset_questionset in instance.questionset_questionsets.all()[:1]]
        questions = [{
            'question': questionset_question.question.id,
            'order': questionset_question.order
        } for questionset_question in instance.questionset_questions.all()[:1]]
        conditions = [condition.pk for condition in instance.conditions.all()[:1]]

        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': '%s_new_%s' % (instance.uri_path, username),
            'comment': instance.comment,
            'attribute': instance.attribute.pk if instance.attribute else '',
            'is_collection': instance.is_collection,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'help_en': instance.help_lang1,
            'help_de': instance.help_lang2,
            'verbose_name_en': instance.verbose_name_lang1,
            'verbose_name_de': instance.verbose_name_lang2,
            'verbose_name_plural_en': instance.verbose_name_plural_lang1,
            'verbose_name_plural_de': instance.verbose_name_plural_lang2,
            'questionsets': questionsets,
            'questions': questions,
            'conditions': conditions
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()

        if response.status_code == 201:
            new_instance = QuestionSet.objects.get(id=response.json().get('id'))
            assert questionsets == [{
                'questionset': questionset_questionset.questionset.id,
                'order': questionset_questionset.order
            } for questionset_questionset in new_instance.questionset_questionsets.all()]
            assert questions == [{
                'question': questionset_question.question.id,
                'order': questionset_question.order
            } for questionset_question in new_instance.questionset_questions.all()]
            assert conditions == [condition.pk for condition in new_instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.all()

    for instance in instances:
        pages = [page.id for page in instance.pages.all()]
        parents = [parent.id for parent in instance.parents.all()]
        questionsets = [questionset.id for questionset in instance.questionsets.all()]
        questions = [question.id for question in instance.questions.all()]
        conditions = [condition.pk for condition in instance.conditions.all()]

        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'attribute': instance.attribute.pk if instance.attribute else None,
            'is_collection': instance.is_collection,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'help_en': instance.help_lang1,
            'help_de': instance.help_lang2,
            'verbose_name_en': instance.verbose_name_lang1,
            'verbose_name_de': instance.verbose_name_lang2,
            'verbose_name_plural_en': instance.verbose_name_plural_lang1,
            'verbose_name_plural_de': instance.verbose_name_plural_lang2
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()

        instance.refresh_from_db()
        assert pages == [page.id for page in instance.pages.all()]
        assert parents == [parent.id for parent in instance.parents.all()]
        assert questionsets == [questionset.id for questionset in instance.questionsets.all()]
        assert questions == [question.id for question in instance.questions.all()]
        assert conditions == [condition.pk for condition in instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_update_m2m(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.all()

    for instance in instances:
        questionsets = [{
            'questionset': questionset_questionset.questionset.id,
            'order': questionset_questionset.order
        } for questionset_questionset in instance.questionset_questionsets.all()[:1]]
        questions = [{
            'question': questionset_question.question.id,
            'order': questionset_question.order
        } for questionset_question in instance.questionset_questions.all()[:1]]
        conditions = [condition.pk for condition in instance.conditions.all()[:1]]

        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': instance.uri_path,
            'comment': instance.comment,
            'attribute': instance.attribute.pk if instance.attribute else None,
            'is_collection': instance.is_collection,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'help_en': instance.help_lang1,
            'help_de': instance.help_lang2,
            'verbose_name_en': instance.verbose_name_lang1,
            'verbose_name_de': instance.verbose_name_lang2,
            'verbose_name_plural_en': instance.verbose_name_plural_lang1,
            'verbose_name_plural_de': instance.verbose_name_plural_lang2,
            'questionsets': questionsets,
            'questions': questions,
            'conditions': conditions
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()

        if response.status_code == 200:
            instance.refresh_from_db()
            assert questionsets == [{
                'questionset': questionset_questionset.questionset.id,
                'order': questionset_questionset.order
            } for questionset_questionset in instance.questionset_questionsets.all()]
            assert questions == [{
                'question': questionset_question.question.id,
                'order': questionset_question.order
            } for questionset_question in instance.questionset_questions.all()]
            assert conditions == [condition.pk for condition in instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_detail_export(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail_export'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['list'][username], response.content

        if response.status_code == 200:
            root = et.fromstring(response.content)
            assert root.tag == 'rdmo'
            for child in root:
                assert child.tag in ['questionset', 'question']


@pytest.mark.parametrize('username,password', users)
def test_copy(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['copy'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix + '-',
            'uri_path': instance.uri_path + '-'
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_copy_wrong(db, client, username, password):
    client.login(username=username, password=password)
    instance = QuestionSet.objects.first()

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

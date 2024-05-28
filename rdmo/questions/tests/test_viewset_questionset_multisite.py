import xml.etree.ElementTree as et

import pytest

from django.db.models import Max
from django.urls import reverse

from rdmo.core.tests import get_obj_perms_status_code
from rdmo.core.tests import multisite_status_map as status_map
from rdmo.core.tests import multisite_users as users

from ..models import QuestionSet
from .test_viewset_questionset import export_formats, urlnames


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
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['nested'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'uri_path': f'{instance.uri_path}_new_{username}',
            'comment': instance.comment,
            'attribute': instance.attribute.pk if instance.attribute else '',
            'is_collection': instance.is_collection,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'help_en': instance.help_lang1,
            'help_de': instance.help_lang2,
            'verbose_name_en': instance.verbose_name_lang1,
            'verbose_name_de': instance.verbose_name_lang2
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_page(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.all()

    for instance in instances:
        page = instance.pages.first()
        if page is not None:
            page_questionsets = list(page.page_questionsets.values_list('questionset', 'order'))
            order = page.page_questionsets.aggregate(order=Max('order')).get('order') + 1

            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'uri_path': f'{instance.uri_path}_new_{username}',
                'comment': instance.comment,
                'attribute': instance.attribute.pk if instance.attribute else '',
                'is_collection': instance.is_collection,
                'title_en': instance.title_lang1,
                'title_de': instance.title_lang2,
                'help_en': instance.help_lang1,
                'help_de': instance.help_lang2,
                'verbose_name_en': instance.verbose_name_lang1,
                'verbose_name_de': instance.verbose_name_lang2,
                'pages': [page.id]
            }
            response = client.post(url, data, content_type='application/json')
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = QuestionSet.objects.get(id=response.json().get('id'))
                page.refresh_from_db()
                assert [*page_questionsets, (new_instance.id, order)] == \
                    list(page.page_questionsets.values_list('questionset', 'order'))


@pytest.mark.parametrize('username,password', users)
def test_create_parent(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.all()

    for instance in instances:
        parent = instance.parents.first()
        if parent is not None:
            parent_questionsets = list(parent.questionset_questionsets.values_list('questionset', 'order'))
            order = parent.questionset_questionsets.aggregate(order=Max('order')).get('order') + 1

            url = reverse(urlnames['list'])
            data = {
                'uri_prefix': instance.uri_prefix,
                'uri_path': f'{instance.uri_path}_new_{username}',
                'comment': instance.comment,
                'attribute': instance.attribute.pk if instance.attribute else '',
                'is_collection': instance.is_collection,
                'title_en': instance.title_lang1,
                'title_de': instance.title_lang2,
                'help_en': instance.help_lang1,
                'help_de': instance.help_lang2,
                'verbose_name_en': instance.verbose_name_lang1,
                'verbose_name_de': instance.verbose_name_lang2,
                'parents': [parent.id]
            }
            response = client.post(url, data, content_type='application/json')
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = QuestionSet.objects.get(id=response.json().get('id'))
                parent.refresh_from_db()
                assert [*parent_questionsets, (new_instance.id, order)] == \
                    list(parent.questionset_questionsets.values_list('questionset', 'order'))


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
            'uri_path': f'{instance.uri_path}_new_{username}',
            'comment': instance.comment,
            'attribute': instance.attribute.pk if instance.attribute else '',
            'is_collection': instance.is_collection,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'help_en': instance.help_lang1,
            'help_de': instance.help_lang2,
            'verbose_name_en': instance.verbose_name_lang1,
            'verbose_name_de': instance.verbose_name_lang2,
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
            'verbose_name_de': instance.verbose_name_lang2
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == get_obj_perms_status_code(instance, username, 'update'), response.json()

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
            'questionsets': questionsets,
            'questions': questions,
            'conditions': conditions
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == get_obj_perms_status_code(instance, username, 'update'), response.json()

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
        assert response.status_code == get_obj_perms_status_code(instance, username, 'delete'), response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_detail_export(db, client, username, password, export_format):
    client.login(username=username, password=password)
    instance = QuestionSet.objects.first()

    url = reverse(urlnames['detail_export'], args=[instance.pk]) + export_format + '/'
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content

    if response.status_code == 200 and export_format == 'xml':
        root = et.fromstring(response.content)
        assert root.tag == 'rdmo'
        for child in root:
            assert child.tag in ['questionset', 'question']

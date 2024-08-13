import pytest

from django.db.models import Max
from django.urls import reverse

from rdmo.core.tests.constants import multisite_status_map as status_map
from rdmo.core.tests.constants import multisite_users as users
from rdmo.core.tests.utils import get_obj_perms_status_code

from ..models import Page
from .test_viewset_page import export_formats, urlnames


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
def test_export(db, client, username, password, export_format, mocked_convert_text):
    client.login(username=username, password=password)

    url = reverse(urlnames['export']) + export_format + '/'
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Page.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_nested(db, client, username, password):
    client.login(username=username, password=password)
    instances = Page.objects.all()

    for instance in instances:
        url = reverse(urlnames['nested'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Page.objects.all()

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
def test_create_section(db, client, username, password):
    client.login(username=username, password=password)
    instances = Page.objects.all()

    for instance in instances:
        section = instance.sections.first()
        if section is not None:
            section_pages = list(section.section_pages.values_list('page', 'order'))
            order = section.section_pages.aggregate(order=Max('order')).get('order') + 1

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
                'sections': [section.id]
            }
            response = client.post(url, data, content_type='application/json')
            assert response.status_code == status_map['create'][username], response.json()

            if response.status_code == 201:
                new_instance = Page.objects.get(id=response.json().get('id'))
                section.refresh_from_db()
                assert [*section_pages, (new_instance.id, order)] == \
                    list(section.section_pages.values_list('page', 'order'))


@pytest.mark.parametrize('username,password', users)
def test_create_m2m(db, client, username, password):
    client.login(username=username, password=password)
    instances = Page.objects.all()

    for instance in instances:
        page_questionsets = [{
            'questionset': page_questionset.questionset.id,
            'order': page_questionset.order
        } for page_questionset in instance.page_questionsets.all()[:1]]
        page_questions = [{
            'question': page_question.question.id,
            'order': page_question.order
        } for page_question in instance.page_questions.all()[:1]]
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
            'questionsets': page_questionsets,
            'questions': page_questions,
            'conditions': conditions
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()

        if response.status_code == 201:
            new_instance = Page.objects.get(id=response.json().get('id'))
            assert page_questionsets == [{
                'questionset': page_questionset.questionset.id,
                'order': page_questionset.order
            } for page_questionset in new_instance.page_questionsets.all()]
            assert page_questions == [{
                'question': page_question.question.id,
                'order': page_question.order
            } for page_question in new_instance.page_questions.all()]
            assert conditions == [condition.pk for condition in new_instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Page.objects.all()

    for instance in instances:
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
        assert questionsets == [questionset.id for questionset in instance.questionsets.all()]
        assert questions == [question.id for question in instance.questions.all()]
        assert conditions == [condition.pk for condition in instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_update_m2m(db, client, username, password):
    client.login(username=username, password=password)
    instances = Page.objects.all()

    for instance in instances:
        page_questionsets = [{
            'questionset': page_questionset.questionset.id,
            'order': page_questionset.order
        } for page_questionset in instance.page_questionsets.all()[:1]]
        page_questions = [{
            'question': page_question.question.id,
            'order': page_question.order
        } for page_question in instance.page_questions.all()[:1]]
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
            'questionsets': page_questionsets,
            'questions': page_questions,
            'conditions': conditions
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == get_obj_perms_status_code(instance, username, 'update'), response.json()

        if response.status_code == 200:
            instance.refresh_from_db()
            assert page_questionsets == [{
                'questionset': page_questionset.questionset.id,
                'order': page_questionset.order
            } for page_questionset in instance.page_questionsets.all()]
            assert page_questions == [{
                'question': page_question.question.id,
                'order': page_question.order
            } for page_question in instance.page_questions.all()]
            assert conditions == [condition.pk for condition in instance.conditions.all()]


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Page.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == get_obj_perms_status_code(instance, username, 'delete'), response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_detail_export(db, client, username, password, export_format, mocked_convert_text):
    client.login(username=username, password=password)
    instance = Page.objects.first()

    url = reverse(urlnames['detail_export'], args=[instance.pk]) + export_format + '/'
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content

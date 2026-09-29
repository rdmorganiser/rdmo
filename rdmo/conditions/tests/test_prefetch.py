import xml.etree.ElementTree as et

import pytest

from django.urls import reverse

from rdmo.questions.models import Question

from ..models import Condition
from ..prefetch import condition_prefetch
from ..renderers import ConditionRenderer
from ..serializers.export import ConditionExportSerializer
from ..viewsets import ConditionViewSet
from .helpers import URI_PREFIX, create_conditions
from .test_viewset_condition import urlnames


@pytest.mark.performance
def test_prefetch_many_conditions(db, django_assert_num_queries):
    conditions = create_conditions(1100, 'many')
    question = Question.objects.create(uri_prefix=URI_PREFIX, uri_path='many', text_lang1='Many conditions')
    question.conditions.set(conditions)
    expected = [(condition.pk, condition.source.uri, condition.target_option.text_lang1) for condition in conditions]

    with django_assert_num_queries(2):
        question = Question.objects.prefetch_related(condition_prefetch('conditions')).get(pk=question.pk)

    with django_assert_num_queries(0):
        actual = [(condition.pk, condition.source.uri, condition.target_option.text_lang1)
                  for condition in question.conditions.all()]

    assert actual == expected


def test_prefetch_shared_conditions(db, django_assert_num_queries):
    first, second = create_conditions(2, 'shared')
    questions = [Question.objects.create(
        uri_prefix=URI_PREFIX, uri_path=f'shared-{index}', text_lang1=f'Question {index}'
    ) for index in range(3)]
    questions[0].conditions.set([first, second])
    questions[1].conditions.add(second)
    expected = {questions[0].pk: [first.pk, second.pk], questions[1].pk: [second.pk], questions[2].pk: []}

    with django_assert_num_queries(2):
        loaded = list(Question.objects.filter(pk__in=expected).prefetch_related(condition_prefetch('conditions')))

    with django_assert_num_queries(0):
        actual = {question.pk: [condition.pk for condition in question.conditions.all()] for question in loaded}
        for question in loaded:
            for condition in question.conditions.all():
                assert condition.source.uri
                assert condition.target_option.text_lang1

    assert actual == expected


@pytest.mark.parametrize('has_source,has_option', [(True, False), (False, True), (False, False)])
def test_prefetch_nullable_references(db, django_assert_num_queries, has_source, has_option):
    condition, = create_conditions(1, 'nullable')
    source_id = condition.source_id if has_source else None
    option_id = condition.target_option_id if has_option else None
    Condition.objects.filter(pk=condition.pk).update(source_id=source_id, target_option_id=option_id)
    question = Question.objects.create(uri_prefix=URI_PREFIX, uri_path='nullable', text_lang1='Nullable references')
    question.conditions.add(condition)

    with django_assert_num_queries(2):
        question = Question.objects.prefetch_related(condition_prefetch('conditions')).get(pk=question.pk)

    with django_assert_num_queries(0):
        loaded, = question.conditions.all()
        assert loaded.pk == condition.pk
        assert (loaded.source.pk if loaded.source is not None else None) == source_id
        assert (loaded.target_option.pk if loaded.target_option is not None else None) == option_id


@pytest.mark.performance
def test_large_condition_export(db, admin_client, django_assert_num_queries):
    conditions = create_conditions(1100, 'export')
    expected_sources = {condition.uri: condition.source.uri for condition in conditions}
    expected_options = {condition.target_option.uri: condition.target_option.text_lang1 for condition in conditions}
    expected_parents = {condition.source.uri: condition.source.parent.uri for condition in conditions}
    view = ConditionViewSet()
    view.action = 'export'
    loaded = list(view.get_queryset().filter(uri_prefix=URI_PREFIX))

    context = view.get_export_serializer_context(loaded)

    with django_assert_num_queries(0):
        data = ConditionExportSerializer(loaded, many=True, context=context).data
        ConditionRenderer().render(data, context={'attributes': True, 'options': True})

    response = admin_client.get(reverse(urlnames['export'], kwargs={'export_format': 'xml'}),
                                {'uri_prefix': URI_PREFIX, 'full': '1'})
    assert response.status_code == 200
    document = et.fromstring(response.content)
    uri_key = '{http://purl.org/dc/elements/1.1/}uri'
    exported_conditions = document.findall('condition')
    assert len(exported_conditions) == len(conditions)
    assert {item.attrib[uri_key]: item.find('source').attrib[uri_key]
            for item in exported_conditions} == expected_sources
    assert {item.attrib[uri_key]: item.find('target_option').attrib[uri_key]
            for item in exported_conditions} == {
                condition.uri: condition.target_option.uri for condition in conditions
            }
    attributes = document.findall('attribute')
    assert len(attributes) == 2200
    assert {item.attrib[uri_key] for item in attributes} == set(expected_parents) | set(expected_parents.values())
    assert {item.attrib[uri_key]: item.find('parent').attrib[uri_key]
            for item in attributes if item.attrib[uri_key] in expected_parents} == expected_parents
    assert {item.attrib[uri_key]: item.find("text[@lang='en']").text
            for item in document.findall('option')} == expected_options
    assert [item['target_option']['text_en'] for item in data] == list(expected_options.values())

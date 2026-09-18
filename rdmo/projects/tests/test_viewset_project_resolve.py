import pytest

from django.urls import reverse

from rdmo.conditions.models import Condition
from rdmo.options.models import OptionSet
from rdmo.questions.models import Page, Question, QuestionSet

from ..models import Value

urlnames = {
    'resolve': 'v1-projects:project-resolve',
}

project_id = 1


@pytest.mark.parametrize('element_type,element_model,element_uri', [
    ('page', Page, 'http://example.com/terms/questions/catalog/conditions/text_equal'),
    ('questionset', QuestionSet, 'http://example.com/terms/questions/catalog/conditions/set_set/set'),
    ('question', Question, 'http://example.com/terms/questions/catalog/conditions/set/text'),
    ('optionset', OptionSet, 'http://example.com/terms/options/condition'),
    ('condition', Condition, 'http://example.com/terms/conditions/text_equal_test'),
])
@pytest.mark.parametrize('result', [True, False])
def test_resolve_get(db, client, element_type, element_model, element_uri, result):
    client.login(username='author', password='author')
    element = element_model.objects.get(uri=element_uri)
    condition = element if element_model is Condition else element.conditions.get()
    Value.objects.update_or_create(
        project_id=project_id, snapshot=None, attribute_id=condition.source_id,
        set_prefix='', set_index=0, collection_index=0,
        defaults={'text': condition.target_text if result else 'other'},
    )

    response = client.get(reverse(urlnames['resolve'], args=[project_id]), {element_type: element.id})

    assert response.status_code == 200
    assert response.json() == {'result': result}


@pytest.mark.parametrize('params,result', [
    # question 1: http://example.com/terms/questions/catalog/individual/text/text
    ({'page': -1, 'question': 1}, True),
    # page 63: http://example.com/terms/questions/catalog/conditions/text_empty
    # condition 1: http://example.com/terms/conditions/text_equal_test
    ({'page': 63, 'condition': 1}, True),
    # page 63: http://example.com/terms/questions/catalog/conditions/text_empty
    # condition 2: http://example.com/terms/conditions/text_not_equal_test
    ({'page': 63, 'condition': 2}, False),
    # page 1: http://example.com/terms/questions/catalog/individual/text
    ({'page': 1, 'condition': -1}, True),
])
def test_resolve_get_multiple_selectors(db, client, params, result):
    client.login(username='author', password='author')

    response = client.get(reverse(urlnames['resolve'], args=[project_id]), params)

    assert response.status_code == 200
    assert response.json() == {'result': result}


@pytest.mark.parametrize('snapshot_id,result', [(None, True), (1, False)])
def test_resolve_get_snapshot(db, client, snapshot_id, result):
    client.login(username='author', password='author')
    condition = Condition.objects.get(uri='http://example.com/terms/conditions/text_equal_test')
    # Keep the current answer "test" and change only the fixture snapshot's answer.
    Value.objects.filter(project_id=project_id, snapshot_id=1, attribute_id=condition.source_id).update(text='other')
    params = {'condition': condition.id}
    if snapshot_id is not None:
        params['snapshot'] = snapshot_id

    response = client.get(reverse(urlnames['resolve'], args=[project_id]), params)

    assert response.status_code == 200
    assert response.json() == {'result': result}


@pytest.mark.parametrize('element_type,element_model,element_uri', [
    ('questionset', QuestionSet, 'http://example.com/terms/questions/catalog/conditions/set_set/set'),
    ('question', Question, 'http://example.com/terms/questions/catalog/conditions/set/text'),
])
@pytest.mark.parametrize('set_index,result', [(0, True), (1, False)])
def test_resolve_get_set_context(db, client, element_type, element_model, element_uri, set_index, result):
    client.login(username='author', password='author')
    element = element_model.objects.get(uri=element_uri)
    condition = element.conditions.get()
    if result:
        Value.objects.update_or_create(
            project_id=project_id, snapshot=None, attribute_id=condition.source_id,
            set_prefix='', set_index=set_index, collection_index=0,
            defaults={'text': condition.target_text},
        )

    response = client.get(reverse(urlnames['resolve'], args=[project_id]), {
        element_type: element.id,
        'set_prefix': '',
        'set_index': set_index,
    })

    assert response.status_code == 200
    assert response.json() == {'result': result}


@pytest.mark.parametrize('results', [
    [
        # from: http://example.com/terms/questions/catalog/conditions/set
        # question 104: http://example.com/terms/questions/catalog/conditions/set/text
        {'set_prefix': '', 'set_index': 0, 'element_type': 'questions', 'element_id': 104, 'result': True},
        {'set_prefix': '', 'set_index': 1, 'element_type': 'questions', 'element_id': 104, 'result': False},
    ],
    [
        # from: http://example.com/terms/questions/catalog/conditions/set_set
        # questionset 94: http://example.com/terms/questions/catalog/conditions/set_set/set
        {'set_prefix': '', 'set_index': 0, 'element_type': 'questionsets', 'element_id': 94, 'result': True},
        {'set_prefix': '', 'set_index': 1, 'element_type': 'questionsets', 'element_id': 94, 'result': False},
    ],
    [
        # from: http://example.com/terms/questions/catalog/conditions/set_set_question
        # question 127: http://example.com/terms/questions/catalog/conditions/set_set_question/set/text
        {'set_prefix': '', 'set_index': 0, 'element_type': 'questions', 'element_id': 127, 'result': True},
        {'set_prefix': '', 'set_index': 1, 'element_type': 'questions', 'element_id': 127, 'result': False},
    ]
])
def test_resolve_set(db, client, results):
    client.login(username='author', password='author')

    attribute_id = 114  # http://example.com/terms/domain/conditions/set/bool

    # TODO: maybe move this into the fixture
    for result in results:
        if result['result']:
            Value.objects.update_or_create(
                project_id=project_id,
                snapshot_id=None,
                attribute_id=attribute_id,
                set_prefix=result['set_prefix'],
                set_index=result['set_index'],
                defaults={
                    'text': '1'
                }
            )

    url = reverse(urlnames['resolve'], args=[project_id])
    data = [
        {k: v for k, v in result.items() if k != 'result'}
        for result in results
    ]
    response = client.post(url, data, content_type='application/json')

    assert response.status_code == 200, response.content
    for response_result, result in zip(response.json(), results, strict=True):
        assert response_result == result


@pytest.mark.parametrize('results', [
    [
        # http://example.com/terms/questions/catalog/conditions/optionset
        # optionset 3: http://example.com/terms/options/condition
        {'set_prefix': '', 'set_index': 0, 'element_type': 'optionsets', 'element_id': 3, 'result': True},
    ],
    [
        # http://example.com/terms/questions/catalog/conditions/optionset
        # optionset 3: http://example.com/terms/options/condition
        {'set_prefix': '', 'set_index': 0, 'element_type': 'optionsets', 'element_id': 3, 'result': False},
    ]
])
def test_resolve_optionset(db, client, results):
    client.login(username='author', password='author')

    attribute_id = 120  # http://example.com/terms/domain/conditions/optionset/bool

    # TODO: maybe move this into the fixture
    for result in results:
        if result['result']:
            Value.objects.update_or_create(
                project_id=project_id,
                snapshot_id=None,
                attribute_id=attribute_id,
                set_prefix=result['set_prefix'],
                set_index=result['set_index'],
                defaults={
                    'text': '1'
                }
            )

    url = reverse(urlnames['resolve'], args=[project_id])
    data = [
        {k: v for k, v in result.items() if k != 'result'}
        for result in results
    ]
    response = client.post(url, data, content_type='application/json')

    assert response.status_code == 200, response.content
    for response_result, result in zip(response.json(), results, strict=True):
        assert response_result == result


@pytest.mark.parametrize('text,result', [('contest', True), ('other', False)])
def test_resolve_post_multiple_conditions(db, client, text, result):
    client.login(username='author', password='author')

    question = Question.objects.get(uri='http://example.com/terms/questions/catalog/individual/text/text')
    conditions = Condition.objects.filter(uri__in=(
        'http://example.com/terms/conditions/text_equal_test',
        'http://example.com/terms/conditions/text_contains_test',
    ))
    question.conditions.set(conditions)
    condition = conditions.get(uri='http://example.com/terms/conditions/text_equal_test')
    Value.objects.update_or_create(
        project_id=project_id,
        snapshot_id=None,
        attribute_id=condition.source_id,
        set_prefix='999',
        set_index=0,
        collection_index=0,
        defaults={'text': text},
    )
    results = [{
        'set_prefix': '999',
        'set_index': 0,
        'element_type': 'questions',
        'element_id': question.id,
        'result': result,
    }]
    data = [{key: value for key, value in item.items() if key != 'result'} for item in results]

    response = client.post(reverse(urlnames['resolve'], args=[project_id]), data, content_type='application/json')

    assert response.status_code == 200, response.content
    assert response.json() == results


def test_resolve_post_uses_current_values(db, client):
    client.login(username='author', password='author')

    question = Question.objects.get(uri='http://example.com/terms/questions/catalog/conditions/set/text')
    condition = question.conditions.get()
    value_params = {
        'project_id': project_id,
        'attribute_id': condition.source_id,
        'set_prefix': '',
        'set_index': 999,
        'collection_index': 0,
    }
    Value.objects.update_or_create(snapshot_id=None, defaults={'text': 'other'}, **value_params)
    Value.objects.update_or_create(snapshot_id=1, defaults={'text': condition.target_text}, **value_params)
    results = [{
        'set_prefix': '',
        'set_index': 999,
        'element_type': 'questions',
        'element_id': question.id,
        'result': False,
    }]
    data = [{key: value for key, value in item.items() if key != 'result'} for item in results]

    response = client.post(reverse(urlnames['resolve'], args=[project_id]), data, content_type='application/json')

    assert response.status_code == 200, response.content
    assert response.json() == results

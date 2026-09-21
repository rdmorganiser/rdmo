import pytest

from django.urls import reverse

from rdmo.conditions.models import Condition
from rdmo.options.models import OptionSet
from rdmo.questions.models import Question, QuestionSet

from ..models import Value

urlnames = {
    'project_answers': 'project_answers',
    'project_answers_export': 'project_answers_export',
    'navigation': 'v1-projects:project-navigation',
    'answers': 'v1-projects:project-answers',
    'page_detail': 'v1-projects:project-page-detail',
    'progress': 'v1-projects:project-progress',
    'resolve': 'v1-projects:project-resolve',
}

max_queries = [
    # action, max_queries, url_kwargs
    ('project_answers', 38, {'pk': 1}),
    ('project_answers_export', 31, {'pk': 1, 'format': 'html'}),
    ('navigation', 38, {'pk': 1}),
    ('navigation', 38, {'pk': 1, 'section_id': 1}),
    ('answers', 41, {'pk': 1}),
    ('page_detail', 44, {'parent_lookup_project': 1, 'pk': 1}),
    ('page_detail', 48, {'parent_lookup_project': 1, 'pk': 42}),
    ('page_detail', 60, {'parent_lookup_project': 1, 'pk': 87}),
    ('progress', 42, {'pk': 1}),
]


@pytest.mark.performance
@pytest.mark.parametrize('action,max_queries,url_kwargs', max_queries)
def test_queries(db, client, django_assert_max_num_queries, action, max_queries, url_kwargs):
    client.login(username='owner', password='owner')
    url = reverse(urlnames[action], kwargs=url_kwargs)

    with django_assert_max_num_queries(max_queries):
        if action == 'progress':
            response = client.post(url)
        else:
            response = client.get(url)

    assert response.status_code == 200


@pytest.mark.performance
@pytest.mark.parametrize('params,result,max_queries', [
    ({}, False, 15),
    ({'page': -1}, False, 16),
    ({'page': 1}, True, 17),
])
def test_resolve_get_without_values_queries(db, client, django_assert_max_num_queries, params, result, max_queries):
    client.login(username='owner', password='owner')

    with django_assert_max_num_queries(max_queries) as queries:
        response = client.get(reverse(urlnames['resolve'], kwargs={'pk': 1}), params)

    assert response.status_code == 200
    assert response.json() == {'result': result}
    assert not any(Value._meta.db_table in query['sql'] for query in queries)


@pytest.mark.performance
def test_resolve_queries(db, client, django_assert_max_num_queries):
    client.login(username='owner', password='owner')
    url = reverse(urlnames['resolve'], kwargs={'pk': 1})
    questionset = QuestionSet.objects.get(
        uri='http://example.com/terms/questions/catalog/conditions/set_set/set'
    )
    question = Question.objects.get(uri='http://example.com/terms/questions/catalog/conditions/set/text')
    optionset = OptionSet.objects.get(uri='http://example.com/terms/options/condition')
    params = [
        {
            'set_prefix': '',
            'set_index': 0,
            'element_type': 'questionsets',
            'element_id': questionset.id,
        },
        {
            'set_prefix': '',
            'set_index': 0,
            'element_type': 'questions',
            'element_id': question.id,
        },
        {
            'set_prefix': '',
            'set_index': 0,
            'element_type': 'optionsets',
            'element_id': optionset.id,
        },
    ]

    with django_assert_max_num_queries(19):
        response = client.post(url, params, content_type='application/json')

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 3
    assert [result['result'] for result in results] == [False, False, False]


@pytest.mark.performance
def test_resolve_empty_queries(db, client, django_assert_max_num_queries):
    client.login(username='owner', password='owner')
    url = reverse(urlnames['resolve'], kwargs={'pk': 1})

    with django_assert_max_num_queries(14) as queries:
        response = client.post(url, [], content_type='application/json')

    assert response.status_code == 200
    assert response.json() == []
    assert not any(Value._meta.db_table in query['sql'] for query in queries)


@pytest.mark.performance
def test_resolve_visible_project_queries(db, client, django_assert_max_num_queries):
    client.login(username='user', password='user')

    with django_assert_max_num_queries(14) as queries:
        response = client.post(
            reverse(urlnames['resolve'], kwargs={'pk': 12}), [], content_type='application/json'
        )

    assert response.status_code == 200
    assert response.json() == []
    assert not any(Value._meta.db_table in query['sql'] for query in queries)


@pytest.mark.performance
def test_resolve_without_sources_queries(db, client, django_assert_max_num_queries):
    client.login(username='owner', password='owner')
    condition = Condition.objects.create(
        uri_prefix='http://example.com/terms', uri_path='resolve-without-source',
        source=None, relation=Condition.RELATION_EMPTY,
    )
    params = [{
        'set_prefix': '', 'set_index': 0,
        'element_type': 'conditions', 'element_id': condition.id,
    }]

    with django_assert_max_num_queries(15) as queries:
        response = client.post(
            reverse(urlnames['resolve'], kwargs={'pk': 1}), params, content_type='application/json'
        )

    assert response.status_code == 200
    assert response.json() == [{**params[0], 'result': False}]
    assert not any(Value._meta.db_table in query['sql'] for query in queries)


@pytest.mark.performance
@pytest.mark.parametrize('element_type', ['pages', 'questionsets', 'questions', 'optionsets', 'conditions'])
def test_resolve_missing_element_queries(db, client, django_assert_max_num_queries, element_type):
    client.login(username='owner', password='owner')
    params = [{
        'set_prefix': '',
        'set_index': 0,
        'element_type': element_type,
        'element_id': -1,
    }]

    with django_assert_max_num_queries(15) as queries:
        response = client.post(
            reverse(urlnames['resolve'], kwargs={'pk': 1}), params, content_type='application/json'
        )

    assert response.status_code == 200
    assert response.json()[0]['result'] is False
    assert not any(Value._meta.db_table in query['sql'] for query in queries)

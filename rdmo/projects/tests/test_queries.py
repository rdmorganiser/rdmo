import pytest

from django.urls import reverse

from .test_viewset_project import urlnames

max_queries = [
    # action, max_queries, url_kwargs, url_params
    ('project_answers', 38, {'pk': 1}, {}),
    ('project_answers_export', 31, {'pk': 1, 'format': 'html'}, {}),
    ('navigation', 38, {'pk': 1}, {}),
    ('navigation', 38, {'pk': 1, 'section_id': 1}, {}),
    ('answers', 41, {'pk': 1}, {}),
    ('page_detail', 44, {'parent_lookup_project': 1, 'pk': 1}, {}),
    ('page_detail', 48, {'parent_lookup_project': 1, 'pk': 42}, {}),
    ('page_detail', 60, {'parent_lookup_project': 1, 'pk': 87}, {}),
    ('progress', 42, {'pk': 1}, {}),
]


@pytest.mark.performance
@pytest.mark.parametrize('action,max_queries,url_kwargs,url_params', max_queries)
def test_queries(db, client, django_assert_max_num_queries, action, max_queries, url_kwargs, url_params):
    client.login(username='owner', password='owner')
    url = reverse(urlnames[action], kwargs=url_kwargs)

    with django_assert_max_num_queries(max_queries):
        if action == 'progress':
            response = client.post(url, query_params=url_params)
        else:
            response = client.get(url, query_params=url_params)

    assert response.status_code == 200


@pytest.mark.performance
def test_resolve_queries(db, client, django_assert_max_num_queries):
    client.login(username='owner', password='owner')
    url = reverse(urlnames['resolve'], kwargs={'pk': 1})
    params = [
        {
            'set_prefix': '',
            'set_index': 0,
            'element_type': 'questionsets',
            'element_id': 94,
        },
        {
            'set_prefix': '',
            'set_index': 0,
            'element_type': 'questions',
            'element_id': 104,
        },
        {
            'set_prefix': '',
            'set_index': 0,
            'element_type': 'optionsets',
            'element_id': 3,
        },
    ]

    with django_assert_max_num_queries(19):
        response = client.post(url, params, content_type='application/json')

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert [result['result'] for result in response.json()] == [False, False, False]


@pytest.mark.performance
def test_resolve_empty_queries(db, client, django_assert_max_num_queries):
    client.login(username='owner', password='owner')
    url = reverse(urlnames['resolve'], kwargs={'pk': 1})

    with django_assert_max_num_queries(14):
        response = client.post(url, [], content_type='application/json')

    assert response.status_code == 200
    assert response.json() == []

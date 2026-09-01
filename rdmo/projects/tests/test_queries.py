import pytest

from django.urls import reverse

from .test_viewset_project import urlnames

max_queries = [
    # action, max_queries, url_kwargs, url_params
    ('project_answers', 38, {'pk': 1}, {}),
    ('project_answers_export', 31, {'pk': 1, 'format': 'html'}, {}),
    ('navigation', 40, {'pk': 1}, {}),
    ('navigation', 40, {'pk': 1, 'section_id': 1}, {}),
    ('answers', 43, {'pk': 1}, {}),
    ('page_detail', 46, {'parent_lookup_project': 1, 'pk': 1}, {}),
    ('page_detail', 50, {'parent_lookup_project': 1, 'pk': 42}, {}),
    ('page_detail', 62, {'parent_lookup_project': 1, 'pk': 87}, {}),
    ('progress', 44, {'pk': 1}, {}),
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
    params = {
        'set_prefix': '',
        'set_index': 0,
        'element_type': 'conditions',
        'element_id': 1,
    }

    with django_assert_max_num_queries(19):
        response = client.post(url, [params, params, params], content_type='application/json')

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0] == response.json()[1] == response.json()[2]

import pytest

from django.urls import reverse

from .test_viewset_condition import urlnames

max_queries = [
    # action, max_queries, url_kwargs
    ('list', 9, {}),
    ('index', 3, {}),
    ('export', 11, {'export_format': 'xml'}),
    ('detail', 9, {'pk': 1}),
    ('detail_export', 9, {'pk': 1, 'export_format': 'xml'}),
]


@pytest.mark.performance
@pytest.mark.parametrize('action,max_queries,url_kwargs', max_queries)
def test_actions_max_query_counts(db, admin_client, django_assert_max_num_queries, action, max_queries, url_kwargs):
    url = reverse(urlnames[action], kwargs=url_kwargs)

    with django_assert_max_num_queries(max_queries):
        response = admin_client.get(url)

    assert response.status_code == 200

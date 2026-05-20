import pytest

from django.urls import reverse

from .test_viewset_view import urlnames

max_queries = [
    # action, max_queries, url_kwargs
    ('list', 8, {}),
    ('index', 3, {}),
    ('export', 10, {'export_format': 'xml'}),
    ('detail', 8, {'pk': 1}),
    ('detail_export', 10, {'pk': 1, 'export_format': 'xml'}),
]

@pytest.mark.performance
@pytest.mark.parametrize('action,max_queries,url_kwargs', max_queries)
def test_views_endpoints_query_counts(
    db,
    admin_client,
    django_assert_max_num_queries,
    action,
    max_queries,
    url_kwargs,
):
    url = reverse(urlnames[action], kwargs=url_kwargs)

    with django_assert_max_num_queries(max_queries):
        response = admin_client.get(url)

    assert response.status_code == 200

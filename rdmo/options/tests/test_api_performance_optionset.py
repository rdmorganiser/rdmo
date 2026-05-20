import pytest

from django.urls import reverse

from .test_viewset_optionsets import urlnames

max_queries = [
    # action, max_queries, url_kwargs
    ('list', 8, {}),
    ('index', 3, {}),
    ('export', 11, {'export_format': 'xml'}),
    ('detail', 8, {'pk': 1}),
    ('detail_export', 10, {'pk': 1, 'export_format': 'xml'}),
]


@pytest.mark.performance
@pytest.mark.parametrize('action,max_queries,url_kwargs', max_queries)
def test_optionset_endpoints_query_counts(
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

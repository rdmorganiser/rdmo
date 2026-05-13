import pytest

from django.urls import reverse

max_query_map = {
    'list': ('v1-domain:attribute-list', {}, 10),
    'index': ('v1-domain:attribute-index', {}, 3),
    'export': ('v1-domain:attribute-export', {'export_format': 'xml'}, 12),
    'detail': ('v1-domain:attribute-detail', {'pk': 1}, 11),
    'detail_export': (
        'v1-domain:attribute-detail-export',
        {'pk': 1, 'export_format': 'xml'},
        12,
    ),
}

@pytest.mark.performance
@pytest.mark.parametrize(
    'url_name,url_kwargs,max_queries',
    [
        (url_name, url_kwargs, max_queries)
        for _, (url_name, url_kwargs, max_queries) in max_query_map.items()
    ],
)
def test_domain_endpoints_query_counts(
    db,
    admin_client,
    django_assert_max_num_queries,
    url_name,
    url_kwargs,
    max_queries,
):
    url = reverse(url_name, kwargs=url_kwargs)

    with django_assert_max_num_queries(max_queries):
        response = admin_client.get(url)
    assert response.status_code == 200

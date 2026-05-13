import pytest

from django.urls import reverse

max_query_map = {
    'list': ('v1-views:view-list', {}, 8),
    'index': ('v1-views:view-index', {}, 3),
    'export': ('v1-views:view-export', {'export_format': 'xml'}, 10),
    'detail': ('v1-views:view-detail', {'pk': 1}, 8),
    'detail_export': (
        'v1-views:view-detail-export',
        {'pk': 1, 'export_format': 'xml'},
        10,
    ),
}

@pytest.mark.performance
@pytest.mark.parametrize(
    'action,url_name,url_kwargs,max_queries',
    [
        (action, url_name, url_kwargs, max_queries)
        for action, (url_name, url_kwargs, max_queries) in max_query_map.items()
    ],
)
def test_views_endpoints_query_counts(
    db,
    admin_client,
    django_assert_max_num_queries,
    action,
    url_name,
    url_kwargs,
    max_queries,
):
    url = reverse(url_name, kwargs=url_kwargs)

    with django_assert_max_num_queries(max_queries):
        response = admin_client.get(url)

    assert response.status_code == 200

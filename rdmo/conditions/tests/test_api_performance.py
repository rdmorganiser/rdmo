import pytest

from django.urls import reverse

max_query_map = {
    # action: url_name url_kwargs max_query_counts
    'list': ('v1-conditions:condition-list', {}, 9),
    'index': ('v1-conditions:condition-index', {}, 3),
    'export': ('v1-conditions:condition-export', {'export_format': 'xml'}, 11),
    'detail': ('v1-conditions:condition-detail', {'pk': 1}, 9),
    'detail_export': ('v1-conditions:condition-detail-export', {'pk': 1, 'export_format': 'xml'}, 9),
}


@pytest.mark.performance
@pytest.mark.parametrize(
    'url_name,url_kwargs,max_queries',
    [
        (url_name, url_kwargs, max_queries)
        for action, (url_name, url_kwargs, max_queries) in max_query_map.items()
    ],
)
def test_conditions_endpoints_query_counts(
    db, admin_client,django_assert_max_num_queries,
    url_name,url_kwargs,max_queries,
):
    url = reverse(url_name, kwargs=url_kwargs)

    with django_assert_max_num_queries(max_queries):
        response = admin_client.get(url)

    assert response.status_code == 200

import pytest

from django.urls import reverse

max_query_map = {
    'list': ('v1-tasks:task-list', {}, 10),
    'index': ('v1-tasks:task-index', {}, 3),
    'export': ('v1-tasks:task-export', {'export_format': 'xml'}, 12),
    'detail': ('v1-tasks:task-detail', {'pk': 1}, 10),
    'detail_export': (
        'v1-tasks:task-detail-export',
        {'pk': 1, 'export_format': 'xml'},
        12,
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
def test_tasks_endpoints_query_counts(
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

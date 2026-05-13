import pytest

from django.urls import reverse

from .test_viewset_page import urlnames

max_query_map = {
    # action: max_queries url_kwargs
    'list': {'max_queries': 10},
    'index': {'max_queries': 3},
    'export': {'max_queries': 25, 'url_kwargs': {'export_format': 'xml'}},
    'detail': {'max_queries': 10, 'url_kwargs': {'pk': 1}},
    'detail_export': {
        'max_queries': 13, 'url_kwargs': {'pk': 1, 'export_format': 'xml'},
    },
}


@pytest.mark.performance
@pytest.mark.parametrize(
    'action,max_queries,url_kwargs',
    [
        (action, case['max_queries'], case.get('url_kwargs'))
        for action, case in max_query_map.items()
    ],
)
def test_page_endpoints_query_counts(
    db, admin_client, django_assert_max_num_queries,
    action, max_queries, url_kwargs,
):
    url = reverse(urlnames[action], kwargs=url_kwargs)

    with django_assert_max_num_queries(max_queries):
        response = admin_client.get(url)

    assert response.status_code == 200

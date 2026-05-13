import pytest

from django.urls import reverse

from .test_viewset_options import urlnames as option_urlnames
from .test_viewset_optionsets import urlnames as optionset_urlnames

max_query_map_optionset = {
    'list': {'max_queries': 8},
    'index': {'max_queries': 3},
    'export': {'max_queries': 11, 'url_kwargs': {'export_format': 'xml'}},
    'detail': {'max_queries': 8, 'url_kwargs': {'pk': 1}},
    'detail_export': {'max_queries': 10, 'url_kwargs': {'pk': 1, 'export_format': 'xml'}},
}

max_query_map_option = {
    'list': {'max_queries': 10},
    'index': {'max_queries': 3},
    'export': {'max_queries': 12, 'url_kwargs': {'export_format': 'xml'}},
    'detail': {'max_queries': 10, 'url_kwargs': {'pk': 1}},
    'detail_export': {'max_queries': 12, 'url_kwargs': {'pk': 1, 'export_format': 'xml'}},
}

@pytest.mark.performance
@pytest.mark.parametrize(
    'action,max_queries,url_kwargs',
    [
        (action, case['max_queries'], case.get('url_kwargs'))
        for action, case in max_query_map_optionset.items()
    ],
)
def test_optionset_endpoints_query_counts(
    admin_client,
    django_assert_max_num_queries,
    action,
    max_queries,
    url_kwargs,
):
    url = reverse(optionset_urlnames[action], kwargs=url_kwargs)
    with django_assert_max_num_queries(max_queries):
        response = admin_client.get(url)
    assert response.status_code == 200


@pytest.mark.performance
@pytest.mark.parametrize(
    'action,max_queries,url_kwargs',
    [
        (action, case['max_queries'], case.get('url_kwargs'))
        for action, case in max_query_map_option.items()
    ],
)
def test_option_endpoints_query_counts(
    admin_client,
    django_assert_max_num_queries,
    action,
    max_queries,
    url_kwargs,
):
    url = reverse(option_urlnames[action], kwargs=url_kwargs)
    with django_assert_max_num_queries(max_queries):
        response = admin_client.get(url)
    assert response.status_code == 200

from urllib.parse import urlencode

import pytest

from django.urls import reverse

from .test_viewset_attribute import urlnames

max_queries = [
    # action, max_queries, url_kwargs, url_params
    ('list', 10, {}, {}),
    ('index', 3, {}, {}),
    ('export', 3, {'export_format': 'xml'}, {}),
    ('export', 3, {'export_format': 'xml'}, {'full': '1'}),
    ('detail', 11, {'pk': 1}, {}),
    ('detail_export', 4, {'pk': 1, 'export_format': 'xml'}, {}),
    ('detail_export', 4, {'pk': 1, 'export_format': 'xml'}, {'full': '1'}),
]


@pytest.mark.performance
@pytest.mark.parametrize("action,max_queries,url_kwargs,url_params", max_queries)
def test_queries(db, admin_client, django_assert_max_num_queries, action, max_queries, url_kwargs, url_params):
    url = reverse(urlnames[action], kwargs=url_kwargs)
    if url_params:
        url += f'?{urlencode(url_params)}'

    with django_assert_max_num_queries(max_queries):
        response = admin_client.get(url)

    assert response.status_code == 200

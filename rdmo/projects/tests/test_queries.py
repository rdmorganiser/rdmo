import pytest

from django.urls import reverse

max_queries = [
    # method, urlname, max_queries, url_args
    ('get', 'v1-projects:project-navigation', 43, [1]),
    ('get', 'v1-projects:project-answers', 43, [1]),
    ('post', 'v1-projects:project-progress', 44, [1]),
    ('get', 'v1-projects:project-page-detail', 46, [1, 1]),
    ('get', 'v1-projects:project-page-detail', 50, [1, 42]),
    ('get', 'v1-projects:project-page-detail', 62, [1, 87]),
]


@pytest.mark.performance
@pytest.mark.parametrize('method,urlname,max_queries,url_args', max_queries)
def test_queries(db, client, django_assert_max_num_queries, method, urlname, max_queries, url_args):
    client.login(username='owner', password='owner')
    url = reverse(urlname, args=url_args)

    with django_assert_max_num_queries(max_queries):
        if method == 'get':
            response = client.get(url)
        elif method == 'post':
            response = client.post(url)

    assert response.status_code == 200

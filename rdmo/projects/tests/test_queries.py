import pytest

from django.urls import reverse

max_queries = {
    # method, urlname, max_queries, url_args
    'owner': (
        ('get', 'v1-projects:project-list', 16, []),
        ('get', 'v1-projects:project-detail', 12, [1]),
        ('get', 'v1-projects:project-navigation', 43, [1]),
        ('get', 'v1-projects:project-answers', 43, [1]),
        ('post', 'v1-projects:project-progress', 44, [1]),
        ('get', 'v1-projects:project-page-detail', 46, [1, 1]),
        ('get', 'v1-projects:project-page-detail', 50, [1, 42]),
        ('get', 'v1-projects:project-page-detail', 62, [1, 87]),
    ),
    'site': (
        ('get', 'v1-projects:project-list', 18, []),              # 2 more
        ('get', 'v1-projects:project-detail', 12, [1]),
        ('get', 'v1-projects:project-navigation', 43, [1]),
        ('get', 'v1-projects:project-answers', 43, [1]),
        ('post', 'v1-projects:project-progress', 44, [1]),
        ('get', 'v1-projects:project-page-detail', 48, [1, 1]),   # 2 more
        ('get', 'v1-projects:project-page-detail', 52, [1, 42]),  # 2 more
        ('get', 'v1-projects:project-page-detail', 64, [1, 87]),  # 2 more
    )
}


@pytest.mark.performance
@pytest.mark.parametrize('method,urlname,max_queries,url_args', max_queries['owner'])
def test_queries_owner(db, client, django_assert_max_num_queries, method, urlname, max_queries, url_args):
    client.login(username='owner', password='owner')
    url = reverse(urlname, args=url_args)

    with django_assert_max_num_queries(max_queries):
        if method == 'get':
            response = client.get(url)
        elif method == 'post':
            response = client.post(url)

    assert response.status_code == 200


@pytest.mark.performance
@pytest.mark.parametrize('method,urlname,max_queries,url_args', max_queries['site'])
def test_queries_site(db, client, django_assert_max_num_queries, method, urlname, max_queries, url_args):
    client.login(username='site', password='site')
    url = reverse(urlname, args=url_args)

    with django_assert_max_num_queries(max_queries):
        if method == 'get':
            response = client.get(url)
        elif method == 'post':
            response = client.post(url)

    assert response.status_code == 200

import pytest

from django.urls import reverse

max_queries = [
    # urlname, max_queries, url_args
    ('project_answers', 41, [1]),
    ('project_answers_export', 34, [1, 'html']),
]

answer_tree_max_queries = [
    # method, urlname, max_queries, url_args
    ('get', 'v1-projects:project-navigation', 46, [1]),
    ('post', 'v1-projects:project-progress', 47, [1]),
    ('get', 'v1-projects:project-page-detail', 60, [1, 1]),
]


@pytest.mark.performance
@pytest.mark.parametrize('urlname,max_queries,url_args', max_queries)
def test_project_answer_endpoints_query_counts(
    db,
    client,
    django_assert_max_num_queries,
    urlname,
    max_queries,
    url_args,
):
    client.login(username='owner', password='owner')
    url = reverse(urlname, args=url_args)

    with django_assert_max_num_queries(max_queries):
        response = client.get(url)

    assert response.status_code == 200


@pytest.mark.performance
@pytest.mark.parametrize('method,urlname,max_queries,url_args', answer_tree_max_queries)
def test_project_answer_tree_endpoints_query_counts(
    db,
    client,
    django_assert_max_num_queries,
    method,
    urlname,
    max_queries,
    url_args,
):
    client.login(username='owner', password='owner')
    url = reverse(urlname, args=url_args)

    with django_assert_max_num_queries(max_queries):
        response = getattr(client, method)(url)

    assert response.status_code == 200

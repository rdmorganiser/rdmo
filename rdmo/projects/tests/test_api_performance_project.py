import pytest

from django.urls import reverse

max_queries = [
    # urlname, max_queries, url_args
    ('project_answers', 41, [1]),
    ('project_answers_export', 34, [1, 'html']),
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

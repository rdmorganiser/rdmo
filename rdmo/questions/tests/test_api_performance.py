import pytest

from django.urls import reverse

# (action, url_name, kwargs, max_queries)
max_queries_mapping = [
    # Catalog endpoints
    ('catalog_list', 'v1-questions:catalog-list', {}, 8),
    ('catalog_index', 'v1-questions:catalog-index', {}, 3),
    ('catalog_export', 'v1-questions:catalog-export', {'export_format': 'xml'}, 30),
    ('catalog_detail', 'v1-questions:catalog-detail', {'pk': 1}, 8),
    ('catalog_detail_export', 'v1-questions:catalog-detail-export',
     {'pk': 1, 'export_format': 'xml'}, 10),

    # Section endpoints
    ('section_list', 'v1-questions:section-list', {}, 8),
    ('section_index', 'v1-questions:section-index', {}, 3),
    ('section_export', 'v1-questions:section-export', {'export_format': 'xml'}, 10),
    ('section_detail', 'v1-questions:section-detail', {'pk': 1}, 8),
    ('section_detail_export', 'v1-questions:section-detail-export',
     {'pk': 1, 'export_format': 'xml'}, 10),

    # Page endpoints
    ('page_list', 'v1-questions:page-list', {}, 10),
    ('page_index', 'v1-questions:page-index', {}, 3),
    ('page_export', 'v1-questions:page-export', {'export_format': 'xml'}, 12),
    ('page_detail', 'v1-questions:page-detail', {'pk': 1}, 10),
    ('page_detail_export', 'v1-questions:page-detail-export',
     {'pk': 1, 'export_format': 'xml'}, 13),

    # Questionset endpoints
    ('questionset_list', 'v1-questions:questionset-list', {}, 11),
    ('questionset_index', 'v1-questions:questionset-index', {}, 3),
    ('questionset_export', 'v1-questions:questionset-export', {'export_format': 'xml'}, 13),
    ('questionset_detail', 'v1-questions:questionset-detail', {'pk': 89}, 10),
    ('questionset_detail_export', 'v1-questions:questionset-detail-export',
     {'pk': 89, 'export_format': 'xml'}, 13),

    # Question endpoints
    ('question_list', 'v1-questions:question-list', {}, 10),
    ('question_index', 'v1-questions:question-index', {}, 3),
    ('question_export', 'v1-questions:question-export', {'export_format': 'xml'}, 12),
    ('question_detail', 'v1-questions:question-detail', {'pk': 1}, 10),
    ('question_detail_export', 'v1-questions:question-detail-export',
     {'pk': 1, 'export_format': 'xml'}, 12),
]

@pytest.mark.performance
@pytest.mark.parametrize('action,url_name,url_kwargs,max_queries', max_queries_mapping)
def test_questions_endpoints_query_counts(db, admin_client, django_assert_max_num_queries,
                                          action, url_name, url_kwargs, max_queries):
    url = reverse(url_name, kwargs=url_kwargs)

    with django_assert_max_num_queries(max_queries):
        response = admin_client.get(url)

    assert response.status_code == 200

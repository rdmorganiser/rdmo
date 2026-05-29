import pytest

from django.urls import reverse

from ..models import Catalog, Page, Question, QuestionSet, Section


@pytest.mark.parametrize(
    'descendant_model,descendant_uri,ancestor_model,ancestor_uri,urlname,ancestor_field,relation_name',
    [
        (
            Section, 'foo-section',
            Catalog, 'foo-catalog',
            'v1-questions:section-list', 'catalogs', 'catalog_sections'
        ),
        (
            Page, 'foo-page',
            Section, 'foo-section',
            'v1-questions:page-list', 'sections', 'section_pages'
        ),
        (
            QuestionSet, 'foo-questionset',
            Page, 'foo-page',
            'v1-questions:questionset-list', 'pages', 'page_questionsets'
        ),
        (
            QuestionSet, 'foo-questionset',
            QuestionSet, 'foo-questionset',
            'v1-questions:questionset-list', 'parents', 'questionset_questionsets'
        ),
        (
            Question, 'foo-question',
            Page, 'foo-page',
            'v1-questions:question-list', 'pages', 'page_questions'
        ),
        (
            Question, 'foo-question',
            QuestionSet, 'foo-questionset',
            'v1-questions:question-list', 'questionsets', 'questionset_questions'
        ),
    ],
    ids=[
        'catalog-to-section',
        'section-to-page',
        'page-to-questionset',
        'questionset-to-questionset',
        'page-to-question',
        'questionset-to-question',
    ],
)
def test_foo_editor_cannot_create_descendant_on_foo_ancestor(
    db, client, descendant_model, descendant_uri, ancestor_model, ancestor_uri, urlname, ancestor_field, relation_name
):
    client.login(username='foo-editor', password='foo-editor')

    descendant = descendant_model.objects.get(uri_path=descendant_uri)
    ancestor = ancestor_model.objects.get(uri_path=ancestor_uri)
    before_count = getattr(ancestor, relation_name).count()

    data = {
        'uri_prefix': 'https://example.com/terms',
        'uri_path': f'{descendant.uri_path}-ancestor-denied',
        ancestor_field: [ancestor.id]
    }
    response = client.post(reverse(urlname), data, content_type='application/json')

    assert response.status_code == 403, response.json()
    assert getattr(ancestor, relation_name).count() == before_count

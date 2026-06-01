import pytest

from django.contrib.sites.models import Site
from django.urls import reverse

from rdmo.core.tests.constants import status_map_object_permissions as status_map

from ..models import Catalog, Page, Question, QuestionSet, Section


@pytest.mark.parametrize('model,parent_model,urlname,payload_builder', [
    (
        Section, Catalog, 'v1-questions:section-list',
        lambda instance, parent: {
            'uri_prefix': 'https://bar.com/terms',
            'uri_path': f'{instance.uri_path}-bar-parent-denied',
            'comment': instance.comment,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'catalogs': [parent.id]
        }
    ),
    (
        Page, Section, 'v1-questions:page-list',
        lambda instance, parent: {
            'uri_prefix': 'https://bar.com/terms',
            'uri_path': f'{instance.uri_path}-bar-parent-denied',
            'comment': instance.comment,
            'attribute': instance.attribute_id,
            'is_collection': instance.is_collection,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'sections': [parent.id]
        }
    ),
    (
        QuestionSet, Page, 'v1-questions:questionset-list',
        lambda instance, parent: {
            'uri_prefix': 'https://bar.com/terms',
            'uri_path': f'{instance.uri_path}-bar-parent-denied',
            'comment': instance.comment,
            'attribute': instance.attribute_id,
            'is_collection': instance.is_collection,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'pages': [parent.id]
        }
    ),
    (
        QuestionSet, QuestionSet, 'v1-questions:questionset-list',
        lambda instance, parent: {
            'uri_prefix': 'https://bar.com/terms',
            'uri_path': f'{instance.uri_path}-bar-parent-denied-parent',
            'comment': instance.comment,
            'attribute': instance.attribute_id,
            'is_collection': instance.is_collection,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'parents': [parent.id]
        }
    ),
    (
        Question, Page, 'v1-questions:question-list',
        lambda instance, parent: {
            'uri_prefix': 'https://bar.com/terms',
            'uri_path': f'{instance.uri_path}-bar-parent-denied',
            'comment': instance.comment,
            'attribute': instance.attribute_id,
            'is_collection': instance.is_collection,
            'is_optional': instance.is_optional,
            'widget_type': instance.widget_type,
            'value_type': instance.value_type,
            'text_en': instance.text_lang1,
            'text_de': instance.text_lang2,
            'pages': [parent.id]
        }
    ),
    (
        Question, QuestionSet, 'v1-questions:question-list',
        lambda instance, parent: {
            'uri_prefix': 'https://bar.com/terms',
            'uri_path': f'{instance.uri_path}-bar-parent-denied-questionset',
            'comment': instance.comment,
            'attribute': instance.attribute_id,
            'is_collection': instance.is_collection,
            'is_optional': instance.is_optional,
            'widget_type': instance.widget_type,
            'value_type': instance.value_type,
            'text_en': instance.text_lang1,
            'text_de': instance.text_lang2,
            'questionsets': [parent.id]
        }
    ),
])
def test_bar_editor_cannot_create_child_on_foo_parent(
    db, client, settings, model, parent_model, urlname, payload_builder
):
    settings.SITE_ID = Site.objects.get(domain='bar.com').id
    Site.objects.clear_cache()
    client.login(username='bar-editor', password='bar-editor')

    parent = parent_model.objects.get(uri_path=f'foo-{parent_model._meta.model_name}')
    instance = model.objects.filter(uri_path=f'foo-{model._meta.model_name}').first()
    if instance is None and model == QuestionSet:
        instance = model.objects.get(uri_path='foo-questionset')
    if instance is None and model == Question:
        instance = model.objects.get(uri_path='foo-question')

    through_name = {
        Catalog: 'catalog_sections',
        Section: 'section_pages',
        Page: 'page_questionsets' if model == QuestionSet else 'page_questions',
        QuestionSet: 'questionset_questionsets' if model == QuestionSet else 'questionset_questions',
    }[parent_model]
    before_count = getattr(parent, through_name).count()
    response = client.post(reverse(urlname), payload_builder(instance, parent), content_type='application/json')

    assert response.status_code == status_map['create-with-parent']['foo-element']['bar-editor'], response.json()
    assert getattr(parent, through_name).count() == before_count

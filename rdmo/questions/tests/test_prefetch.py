import pytest

from django.test import RequestFactory
from django.urls import reverse

from rdmo.conditions.constants import RelationTypes
from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute
from rdmo.options.models import Option, OptionSet, OptionSetOption

from ..models import (
    Catalog,
    CatalogSection,
    Page,
    PageQuestion,
    PageQuestionSet,
    Question,
    QuestionSet,
    QuestionSetQuestion,
    QuestionSetQuestionSet,
    Section,
    SectionPage,
)
from ..serializers.export import PageExportSerializer, QuestionExportSerializer
from ..utils import get_export_flags, get_serializer_context
from ..viewsets import PageViewSet, QuestionViewSet
from .factories import URI_PREFIX, create_element, create_elements
from .test_viewset_page import urlnames as page_urlnames
from .test_viewset_question import urlnames as question_urlnames


@pytest.mark.performance
def test_prefetch_many_catalog_sections(db, django_assert_max_num_queries, django_assert_num_queries):
    catalog = create_element(Catalog, 'query-safety-catalog-sections')
    sections = list(reversed(create_elements(Section, 1100, 'query-safety-catalog-sections-child')))
    CatalogSection.objects.bulk_create([
        CatalogSection(catalog=catalog, section=section, order=order)
        for order, section in enumerate(sections)
    ])
    expected_sections = [(section.pk, order) for order, section in enumerate(sections)]

    with django_assert_max_num_queries(20):
        catalog = Catalog.objects.prefetch_elements().get(pk=catalog.pk)

    with django_assert_num_queries(0):
        actual_sections = [(catalog_section.section.pk, catalog_section.order)
                           for catalog_section in catalog.catalog_sections.all()]
        element_ids = [element.pk for element in catalog.elements]

    assert actual_sections == expected_sections
    assert element_ids == [section.pk for section in sections]


@pytest.mark.performance
def test_prefetch_many_section_pages(db, django_assert_max_num_queries, django_assert_num_queries):
    section = create_element(Section, 'query-safety-section-pages')
    pages = list(reversed(create_elements(Page, 1100, 'query-safety-section-pages-child')))
    SectionPage.objects.bulk_create([
        SectionPage(section=section, page=page, order=order)
        for order, page in enumerate(pages)
    ])
    expected_pages = [(page.pk, order) for order, page in enumerate(pages)]

    with django_assert_max_num_queries(20):
        section = Section.objects.prefetch_elements().get(pk=section.pk)

    with django_assert_num_queries(0):
        actual_pages = [(section_page.page.pk, section_page.order)
                        for section_page in section.section_pages.all()]
        element_ids = [element.pk for element in section.elements]

    assert actual_pages == expected_pages
    assert element_ids == [page.pk for page in pages]


@pytest.mark.performance
def test_prefetch_many_page_questions(db, django_assert_max_num_queries, django_assert_num_queries):
    page = create_element(Page, 'query-safety-page-questions')
    questions = list(reversed(create_elements(Question, 1100, 'query-safety-page-questions-child')))
    PageQuestion.objects.bulk_create([
        PageQuestion(page=page, question=question, order=order)
        for order, question in enumerate(questions)
    ])
    expected_questions = [(question.pk, order) for order, question in enumerate(questions)]

    with django_assert_max_num_queries(20):
        page = Page.objects.prefetch_elements().get(pk=page.pk)

    with django_assert_num_queries(0):
        actual_questions = [(page_question.question.pk, page_question.order)
                            for page_question in page.page_questions.all()]
        element_ids = [element.pk for element in page.elements]

    assert actual_questions == expected_questions
    assert element_ids == [question.pk for question in questions]


@pytest.mark.performance
def test_prefetch_many_page_questionsets(db, django_assert_max_num_queries, django_assert_num_queries):
    page = create_element(Page, 'query-safety-page-questionsets')
    questionsets = list(reversed(create_elements(QuestionSet, 1100, 'query-safety-page-questionsets-child')))
    PageQuestionSet.objects.bulk_create([
        PageQuestionSet(page=page, questionset=questionset, order=order)
        for order, questionset in enumerate(questionsets)
    ])
    expected_questionsets = [(questionset.pk, order) for order, questionset in enumerate(questionsets)]

    with django_assert_max_num_queries(20):
        page = Page.objects.prefetch_elements().get(pk=page.pk)

    with django_assert_num_queries(0):
        actual_questionsets = [(page_questionset.questionset.pk, page_questionset.order)
                               for page_questionset in page.page_questionsets.all()]
        element_ids = [element.pk for element in page.elements]

    assert actual_questionsets == expected_questionsets
    assert element_ids == [questionset.pk for questionset in questionsets]


@pytest.mark.performance
def test_prefetch_many_questionset_questions(db, django_assert_max_num_queries, django_assert_num_queries):
    questionset = create_element(QuestionSet, 'query-safety-questionset-questions')
    questions = list(reversed(create_elements(Question, 1100, 'query-safety-questionset-questions-child')))
    QuestionSetQuestion.objects.bulk_create([
        QuestionSetQuestion(questionset=questionset, question=question, order=order)
        for order, question in enumerate(questions)
    ])
    expected_questions = [(question.pk, order) for order, question in enumerate(questions)]

    with django_assert_max_num_queries(20):
        questionset = QuestionSet.objects.prefetch_elements().get(pk=questionset.pk)

    with django_assert_num_queries(0):
        actual_questions = [(questionset_question.question.pk, questionset_question.order)
                            for questionset_question in questionset.questionset_questions.all()]
        element_ids = [element.pk for element in questionset.elements]

    assert actual_questions == expected_questions
    assert element_ids == [question.pk for question in questions]


@pytest.mark.performance
def test_prefetch_many_questionset_questionsets(db, django_assert_max_num_queries, django_assert_num_queries):
    parent_questionset = create_element(QuestionSet, 'query-safety-questionset-questionsets')
    child_questionsets = list(reversed(create_elements(
        QuestionSet, 1100, 'query-safety-questionset-questionsets-child'
    )))
    QuestionSetQuestionSet.objects.bulk_create([
        QuestionSetQuestionSet(parent=parent_questionset, questionset=child_questionset, order=order)
        for order, child_questionset in enumerate(child_questionsets)
    ])
    expected_child_questionsets = [
        (child_questionset.pk, order) for order, child_questionset in enumerate(child_questionsets)
    ]

    with django_assert_max_num_queries(20):
        parent_questionset = QuestionSet.objects.prefetch_elements().get(pk=parent_questionset.pk)

    with django_assert_num_queries(0):
        actual_child_questionsets = [(questionset_questionset.questionset.pk, questionset_questionset.order)
                                     for questionset_questionset in parent_questionset.questionset_questionsets.all()]
        element_ids = [element.pk for element in parent_questionset.elements]

    assert actual_child_questionsets == expected_child_questionsets
    assert element_ids == [child_questionset.pk for child_questionset in child_questionsets]


@pytest.mark.performance
def test_prefetch_shared_questions_and_page_order(db, django_assert_num_queries):
    first_page = create_element(Page, 'query-safety-shared-first-page')
    second_page = create_element(Page, 'query-safety-shared-second-page')
    question = create_element(Question, 'query-safety-shared-question')
    questionset = create_element(QuestionSet, 'query-safety-shared-questionset')
    unrelated_questions = create_elements(Question, 40, 'query-safety-shared-unrelated-question')
    PageQuestion.objects.create(page=first_page, question=question, order=3)
    PageQuestion.objects.create(page=first_page, question=question, order=4)
    PageQuestionSet.objects.create(page=first_page, questionset=questionset, order=2)
    PageQuestion.objects.create(page=second_page, question=question, order=8)

    pages = Page.objects.filter(pk__in=[first_page.pk, second_page.pk]).prefetch_elements()
    pages_by_id = {page.pk: page for page in pages}
    with django_assert_num_queries(0):
        first_elements = [(type(element), element.pk) for element in pages_by_id[first_page.pk].elements]
        second_elements = [(type(element), element.pk) for element in pages_by_id[second_page.pk].elements]

    assert first_elements == [(QuestionSet, questionset.pk), (Question, question.pk), (Question, question.pk)]
    assert second_elements == [(Question, question.pk)]
    unrelated_elements = {(Question, question.pk) for question in unrelated_questions}
    assert not unrelated_elements.intersection(first_elements + second_elements)


@pytest.mark.performance
def test_prefetch_nested_questionset_descendants(db, django_assert_num_queries):
    parent_questionset = create_element(QuestionSet, 'query-safety-nested-parent')
    child_questionset = create_element(QuestionSet, 'query-safety-nested-child')
    question = create_element(Question, 'query-safety-nested-question')
    QuestionSetQuestionSet.objects.create(parent=parent_questionset, questionset=child_questionset, order=1)
    QuestionSetQuestion.objects.create(questionset=child_questionset, question=question, order=2)

    parent_questionset = QuestionSet.objects.prefetch_elements().get(pk=parent_questionset.pk)
    with django_assert_num_queries(0):
        descendant_ids = [element.pk for element in parent_questionset.descendants]

    assert descendant_ids == [child_questionset.pk, question.pk]


@pytest.mark.performance
def test_prefetch_catalog_to_dict(db, django_assert_max_num_queries, django_assert_num_queries):
    catalog = create_element(Catalog, 'query-safety-catalog-dict')
    section = create_element(Section, 'query-safety-catalog-dict-section')
    page = create_element(Page, 'query-safety-catalog-dict-page')
    parent_questionset = create_element(QuestionSet, 'query-safety-catalog-dict-parent')
    child_questionset = create_element(QuestionSet, 'query-safety-catalog-dict-child')
    question = create_element(Question, 'query-safety-catalog-dict-question')
    CatalogSection.objects.create(catalog=catalog, section=section, order=1)
    SectionPage.objects.create(section=section, page=page, order=1)
    PageQuestionSet.objects.create(page=page, questionset=parent_questionset, order=1)
    QuestionSetQuestionSet.objects.create(parent=parent_questionset, questionset=child_questionset, order=1)
    QuestionSetQuestion.objects.create(questionset=child_questionset, question=question, order=1)

    catalog = Catalog.objects.get(pk=catalog.pk)
    with django_assert_max_num_queries(20):
        catalog.prefetch_elements()
    with django_assert_num_queries(0):
        data = catalog.to_dict()

    section_data = data['elements'][0]
    page_data = section_data['elements'][0]
    parent_questionset_data = page_data['elements'][0]
    child_questionset_data = parent_questionset_data['elements'][0]
    question_data = child_questionset_data['elements'][0]
    assert data['id'] == catalog.pk
    assert section_data['id'] == section.pk
    assert page_data['id'] == page.pk
    assert parent_questionset_data['id'] == parent_questionset.pk
    assert child_questionset_data['id'] == child_questionset.pk
    assert question_data['id'] == question.pk


@pytest.mark.performance
def test_prefetch_many_question_attributes_and_defaults(db, django_assert_max_num_queries, django_assert_num_queries):
    options = create_elements(Option, 1100, 'query-safety-question-default-option')
    questions = []
    expected_references = {}
    for index, option in enumerate(options):
        attribute = Attribute.objects.create(uri_prefix=URI_PREFIX, key=f'query-safety-question-attribute-{index}')
        question = create_element(
            Question, f'query-safety-question-references-{index}', attribute=attribute, default_option=option
        )
        questions.append(question)
        expected_references[question.pk] = (attribute.pk, option.pk)

    question_ids = [question.pk for question in questions]
    with django_assert_max_num_queries(4):
        questions = list(Question.objects.filter(pk__in=question_ids).select_related(
            'attribute', 'default_option'
        ).prefetch_elements())
    with django_assert_num_queries(0):
        actual_references = {
            question.pk: (question.attribute.pk, question.default_option.pk)
            for question in questions
        }

    assert actual_references == expected_references


def test_prefetch_question_options_and_default(db, django_assert_num_queries):
    attribute = Attribute.objects.create(uri_prefix=URI_PREFIX, key='question-options-attribute')
    default_option = create_element(Option, 'question-options-default')
    option = create_element(Option, 'question-options-member')
    optionset = create_element(OptionSet, 'question-options-set')
    OptionSetOption.objects.create(optionset=optionset, option=option, order=1)
    question = create_element(
        Question, 'question-options', attribute=attribute, default_option=default_option
    )
    question.optionsets.add(optionset)

    question = Question.objects.prefetch_elements(options=True).get(pk=question.pk)

    with django_assert_num_queries(0):
        assert question.attribute.uri == attribute.uri
        assert question.default_option.uri == default_option.uri
        assert question.default_option.text_lang1 == default_option.text_lang1
        loaded_optionset, = question.optionsets.all()
        assert loaded_optionset.pk == optionset.pk
        assert [(association.option.uri, association.option.text_lang1, association.order)
                for association in loaded_optionset.optionset_options.all()] == [(option.uri, option.text_lang1, 1)]


@pytest.mark.performance
def test_question_export_default_option_without_expansion(
    db, admin_client, django_assert_max_num_queries, django_assert_num_queries
):
    default_option = create_element(Option, 'query-safety-question-export-default')
    other_option = create_element(Option, 'query-safety-question-export-other')
    optionset = create_element(OptionSet, 'query-safety-question-export-optionset')
    OptionSetOption.objects.create(optionset=optionset, option=other_option, order=1)
    question = create_element(
        Question, 'query-safety-question-export', default_option=default_option,
        help_lang1='Question export help',
    )
    question.optionsets.add(optionset)

    params = {'optionsets': '0', 'options': '0'}
    view = QuestionViewSet()
    view.action = 'export'
    view.request = RequestFactory().get('/export/', params)
    flags = get_export_flags(view.request)

    with django_assert_max_num_queries(3):
        questions = list(view.get_queryset().filter(pk=question.pk))
    with django_assert_num_queries(0):
        context = get_serializer_context(questions, flags)
        data = QuestionExportSerializer(questions, many=True, context=context).data

    assert data[0]['default_option'] == default_option.uri
    assert data[0]['optionsets'] == [{'uri': optionset.uri}]
    assert data[0]['text_en'] == question.text_lang1
    assert data[0]['help_en'] == question.help_lang1

    url = reverse(question_urlnames['export']) + 'xml/'
    response = admin_client.get(url, {'uri': question.uri, **params})
    assert response.status_code == 200
    assert default_option.uri.encode() in response.content
    assert question.text_lang1.encode() in response.content
    assert question.help_lang1.encode() in response.content
    assert other_option.uri.encode() not in response.content


@pytest.mark.performance
def test_page_export_default_option_without_expansion(
    db, admin_client, django_assert_max_num_queries, django_assert_num_queries
):
    default_option = create_element(Option, 'query-safety-page-export-default')
    other_option = create_element(Option, 'query-safety-page-export-other')
    optionset = create_element(OptionSet, 'query-safety-page-export-optionset')
    OptionSetOption.objects.create(optionset=optionset, option=other_option, order=1)
    question = create_element(
        Question, 'query-safety-page-export-question', default_option=default_option,
        help_lang1='Page question export help',
    )
    question.optionsets.add(optionset)
    page = create_element(Page, 'query-safety-page-export', help_lang1='Page export help')
    PageQuestion.objects.create(page=page, question=question, order=1)

    params = {'optionsets': '0', 'options': '0'}
    view = PageViewSet()
    view.action = 'export'
    view.request = RequestFactory().get('/export/', params)
    flags = get_export_flags(view.request)

    with django_assert_max_num_queries(6):
        pages = list(view.get_queryset().filter(pk=page.pk))
    with django_assert_num_queries(0):
        context = get_serializer_context(pages, flags)
        data = PageExportSerializer(pages, many=True, context=context).data

    exported_question = data[0]['page_questions'][0]['question']
    assert data[0]['title_en'] == page.title_lang1
    assert data[0]['help_en'] == page.help_lang1
    assert exported_question['default_option'] == default_option.uri
    assert exported_question['optionsets'] == [{'uri': optionset.uri}]
    assert exported_question['text_en'] == question.text_lang1
    assert exported_question['help_en'] == question.help_lang1

    url = reverse(page_urlnames['export']) + 'xml/'
    response = admin_client.get(url, {'uri': page.uri, **params})
    assert response.status_code == 200
    assert default_option.uri.encode() in response.content
    assert page.title_lang1.encode() in response.content
    assert page.help_lang1.encode() in response.content
    assert question.text_lang1.encode() in response.content
    assert question.help_lang1.encode() in response.content
    assert other_option.uri.encode() not in response.content


@pytest.mark.performance
def test_prefetch_condition_references(db, django_assert_max_num_queries, django_assert_num_queries):
    source = Attribute.objects.create(uri_prefix=URI_PREFIX, key='query-safety-condition-source')
    option = create_element(Option, 'query-safety-condition-option')
    condition = Condition.objects.create(
        uri_prefix=URI_PREFIX, uri_path='query-safety-condition', source=source,
        target_option=option, relation=RelationTypes.RELATION_EQUAL,
    )
    question = create_element(Question, 'query-safety-condition-question')
    question.conditions.add(condition)

    with django_assert_max_num_queries(3):
        question = Question.objects.prefetch_elements().get(pk=question.pk)
    with django_assert_num_queries(0):
        references = [(condition.uri, condition.source.uri, condition.target_option.uri)
                      for condition in question.conditions.all()]

    assert references == [(condition.uri, source.uri, option.uri)]


@pytest.mark.performance
@pytest.mark.parametrize('question_count', [4, 40])
def test_prefetch_page_query_count(db, django_assert_num_queries, question_count):
    page = create_element(Page, 'query-safety-page-query-count')
    questions = create_elements(Question, question_count, 'query-safety-page-query-count-question')
    PageQuestion.objects.bulk_create([
        PageQuestion(page=page, question=question, order=order)
        for order, question in enumerate(questions)
    ])
    expected_questions = [question.pk for question in questions]

    with django_assert_num_queries(5):
        page = Page.objects.prefetch_elements().get(pk=page.pk)
    with django_assert_num_queries(0):
        actual_questions = [question.pk for question in page.elements]

    assert actual_questions == expected_questions


@pytest.mark.parametrize('through_page', [False, True])
def test_prefetch_optionset_conditions(db, django_assert_num_queries, through_page):
    source = Attribute.objects.create(uri_prefix=URI_PREFIX, key='optionset-condition-source')
    option = create_element(Option, 'optionset-condition-target')
    condition = create_element(Condition, 'optionset-condition', source=source, target_option=option, relation='eq')
    optionset = create_element(OptionSet, 'optionset-condition-set')
    optionset.conditions.add(condition)
    question = create_element(Question, 'optionset-condition-question')
    question.optionsets.add(optionset)
    page = create_element(Page, 'optionset-condition-page')
    PageQuestion.objects.create(page=page, question=question, order=0)

    if through_page:
        with django_assert_num_queries(7):
            loaded = Page.objects.prefetch_elements(optionsets_conditions=True).get(pk=page.pk)
    else:
        with django_assert_num_queries(4):
            loaded = Question.objects.prefetch_elements(optionsets_conditions=True).get(pk=question.pk)

    with django_assert_num_queries(0):
        if through_page:
            association, = loaded.page_questions.all()
            assert association.order == 0
            loaded = association.question
        assert loaded.pk == question.pk
        loaded_optionset, = loaded.optionsets.all()
        assert loaded_optionset.pk == optionset.pk
        loaded_condition, = loaded_optionset.conditions.all()
        assert loaded_condition.pk == condition.pk
        assert loaded_condition.source.uri == source.uri
        assert loaded_condition.target_option.uri == option.uri
        assert loaded_condition.target_option.text_lang1 == option.text_lang1

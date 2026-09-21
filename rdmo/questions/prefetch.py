from django.db.models import Prefetch

from rdmo.conditions.prefetch import condition_prefetch
from rdmo.options.prefetch import optionset_options_prefetch


def get_catalog_prefetch_lookups(**kwargs):
    return (
        catalog_section_prefetch('catalog_sections', **kwargs),
    )


def get_section_prefetch_lookups(**kwargs):
    return (
        section_page_prefetch('section_pages', **kwargs),
    )


def get_page_prefetch_lookups(**kwargs):
    return (
        condition_prefetch('conditions'),
        page_question_prefetch('page_questions', **kwargs),
        page_questionset_prefetch('page_questionsets', **kwargs),
    )


def get_questionset_prefetch_lookups(**kwargs):
    return (
        condition_prefetch('conditions'),
        questionset_question_prefetch('questionset_questions', **kwargs),
        questionset_questionset_prefetch('questionset_questionsets', **kwargs),
    )


def get_question_prefetch_lookups(optionsets=False, optionsets_conditions=False, options=False):
    additional_lookups = []
    if optionsets:
        additional_lookups += [
            'optionsets',
        ]
    if optionsets_conditions:
        additional_lookups += [
            condition_prefetch('optionsets__conditions'),
        ]
    if options:
        additional_lookups += [
            'default_option',
            optionset_options_prefetch('optionsets__optionset_options'),
        ]

    return (
        'attribute',
        condition_prefetch('conditions'),
        *additional_lookups
    )


def catalog_section_prefetch(lookup, **kwargs):
    from .models import CatalogSection

    return Prefetch(
        lookup,
        queryset=CatalogSection.objects.select_related('section').prefetch_related(
            section_page_prefetch('section__section_pages', **kwargs),
        )
    )


def section_page_prefetch(lookup, **kwargs):
    from .models import SectionPage

    return Prefetch(
        lookup,
        queryset=SectionPage.objects.select_related(
            'page', 'page__attribute',
        ).prefetch_related(
            condition_prefetch('page__conditions'),
            page_question_prefetch('page__page_questions', **kwargs),
            page_questionset_prefetch('page__page_questionsets', **kwargs),
        )
    )


def page_questionset_prefetch(lookup, **kwargs):
    from .models import PageQuestionSet

    return Prefetch(
        lookup,
        queryset=PageQuestionSet.objects.select_related(
            'questionset', 'questionset__attribute',
        ).prefetch_related(
            condition_prefetch('questionset__conditions'),
            questionset_question_prefetch('questionset__questionset_questions', **kwargs),
            questionset_questionset_prefetch('questionset__questionset_questionsets', **kwargs),
        )
    )


def questionset_questionset_prefetch(lookup, **kwargs):
    from .models import QuestionSetQuestionSet

    return Prefetch(
        lookup,
        queryset=QuestionSetQuestionSet.objects.select_related(
            'questionset', 'questionset__attribute',
        ).prefetch_related(
            condition_prefetch('questionset__conditions'),
            questionset_question_prefetch('questionset__questionset_questions', **kwargs),
            # Stop here instead of recursively constructing an unbounded QuestionSet prefetch tree.
        )
    )


def page_question_prefetch(lookup, **kwargs):
    from .models import PageQuestion

    return _question_through_prefetch(lookup, PageQuestion, **kwargs)


def questionset_question_prefetch(lookup, **kwargs):
    from .models import QuestionSetQuestion

    return _question_through_prefetch(lookup, QuestionSetQuestion, **kwargs)


def _question_through_prefetch(lookup, through_model, optionsets=False, optionsets_conditions=False, options=False):
    """Prefetch a PageQuestion or QuestionSetQuestion relation and its Question."""
    additional_fields = ['question__default_option'] if options else []
    additional_lookups = []
    if optionsets:
        additional_lookups += [
            'question__optionsets',
        ]
    if optionsets_conditions:
        additional_lookups += [
            condition_prefetch('question__optionsets__conditions'),
        ]
    if options:
        additional_lookups += [
            optionset_options_prefetch('question__optionsets__optionset_options'),
        ]

    return Prefetch(
        lookup,
        queryset=through_model.objects.select_related(
            'question', 'question__attribute',
            *additional_fields,
        ).prefetch_related(
            condition_prefetch('question__conditions'),
            *additional_lookups,
        )
    )

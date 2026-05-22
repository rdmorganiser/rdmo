from django.db.models import Prefetch

from rdmo.conditions.models import Condition


def get_catalog_prefetch_lookups(**kwargs):
    return (
        section_prefetch('catalog_sections__section', **kwargs),
    )


def get_section_prefetch_lookups(**kwargs):
    return (
        page_prefetch('section_pages__page', **kwargs),
    )


def get_page_prefetch_lookups(**kwargs):
    return (
        condition_prefetch('conditions'),
        question_prefetch('page_questions__question', **kwargs),
        questionset_prefetch('page_questionsets__questionset', **kwargs),
    )


def get_questionset_prefetch_lookups(**kwargs):
    return (
        condition_prefetch('conditions'),
        question_prefetch('questionset_questions__question', **kwargs),
        questionset_questionset_prefetch('questionset_questionsets__questionset', **kwargs),
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
            'optionsets__optionset_options__option',
        ]

    return (
        'attribute',
        condition_prefetch('conditions'),
        *additional_lookups
    )


def section_prefetch(lookup, **kwargs):
    from .models import Section

    return Prefetch(
        lookup,
        queryset=Section.objects.prefetch_related(
            page_prefetch('section_pages__page', **kwargs),
        )
    )


def page_prefetch(lookup, **kwargs):
    from .models import Page

    return Prefetch(
        lookup,
        queryset=Page.objects.select_related(
            'attribute',
        ).prefetch_related(
            condition_prefetch('conditions'),
            question_prefetch('page_questions__question', **kwargs),
            questionset_prefetch('page_questionsets__questionset', **kwargs),
        )
    )


def questionset_prefetch(lookup, **kwargs):
    from .models import QuestionSet

    return Prefetch(
        lookup,
        queryset=QuestionSet.objects.select_related(
            'attribute',
        ).prefetch_related(
            condition_prefetch('conditions'),
            question_prefetch('questionset_questions__question', **kwargs),
            questionset_questionset_prefetch('questionset_questionsets__questionset', **kwargs),
        )
    )


def questionset_questionset_prefetch(lookup, **kwargs):
    from .models import QuestionSet

    return Prefetch(
        lookup,
        queryset=QuestionSet.objects.select_related(
            'attribute',
        ).prefetch_related(
            condition_prefetch('conditions'),
            question_prefetch('questionset_questions__question', **kwargs),
        )
    )


def question_prefetch(lookup, optionsets=False, optionsets_conditions=False, options=False):
    from .models import Question

    additional_fields = ['default_option'] if options else []
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
            'optionsets__optionset_options__option',
        ]

    return Prefetch(
        lookup,
        queryset=Question.objects.select_related(
            'attribute',
            *additional_fields,
        ).prefetch_related(
            condition_prefetch('conditions'),
            *additional_lookups,
        )
    )


def condition_prefetch(lookup):
    return Prefetch(
        lookup,
        queryset=Condition.objects.select_related('source', 'target_option')
    )

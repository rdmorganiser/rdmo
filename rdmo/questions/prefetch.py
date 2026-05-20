from django.db.models import Prefetch

from rdmo.conditions.models import Condition


def condition_prefetch(path):
    return Prefetch(
        path,
        queryset=Condition.objects.select_related('source', 'source__parent', 'target_option')
    )


def question_options_prefetch_lookups():
    return (
        'optionsets',
        'optionsets__optionset_options__option',
    )


def question_prefetch(path, include_options=False):
    from .models import Question

    optionset_lookups = question_options_prefetch_lookups() if include_options else ('optionsets',)

    return Prefetch(
        path,
        queryset=Question.objects.select_related(
            'attribute',
        ).prefetch_related(
            condition_prefetch('conditions'),
            *optionset_lookups,
        )
    )


def questionset_questionset_prefetch(path):
    from .models import QuestionSet

    return Prefetch(
        path,
        queryset=QuestionSet.objects.select_related(
            'attribute',
        ).prefetch_related(
            condition_prefetch('conditions'),
            question_prefetch('questionset_questions__question'),
        )
    )


def questionset_prefetch(path, include_question_options=False):
    from .models import QuestionSet

    return Prefetch(
        path,
        queryset=QuestionSet.objects.select_related(
            'attribute',
        ).prefetch_related(
            condition_prefetch('conditions'),
            question_prefetch(
                'questionset_questions__question',
                include_options=include_question_options
            ),
            questionset_questionset_prefetch('questionset_questionsets__questionset'),
        )
    )


def page_prefetch(path):
    from .models import Page

    return Prefetch(
        path,
        queryset=Page.objects.select_related(
            'attribute',
        ).prefetch_related(
            condition_prefetch('conditions'),
            question_prefetch('page_questions__question'),
            questionset_prefetch('page_questionsets__questionset'),
        )
    )


def section_prefetch(path):
    from .models import Section

    return Prefetch(
        path,
        queryset=Section.objects.prefetch_related(
            page_prefetch('section_pages__page'),
        )
    )


def catalog_prefetch_lookups():
    return (
        section_prefetch('catalog_sections__section'),
    )


def section_prefetch_lookups():
    return (
        page_prefetch('section_pages__page'),
    )


def page_prefetch_lookups():
    return (
        condition_prefetch('conditions'),
        question_prefetch('page_questions__question'),
        questionset_prefetch('page_questionsets__questionset'),
    )


def project_page_prefetch_lookups():
    return (
        condition_prefetch('conditions'),
        question_prefetch('page_questions__question', include_options=True),
        questionset_prefetch('page_questionsets__questionset', include_question_options=True),
    )


def questionset_prefetch_lookups():
    return (
        condition_prefetch('conditions'),
        question_prefetch('questionset_questions__question'),
        questionset_questionset_prefetch('questionset_questionsets__questionset'),
    )


def question_prefetch_lookups():
    return (
        condition_prefetch('conditions'),
        'optionsets',
        'default_option',
    )

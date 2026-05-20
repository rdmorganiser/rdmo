from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute
from rdmo.questions.models import Page, Question, QuestionSet


def get_export_serializer_context(elements, renderer_context):
    if not any(
        renderer_context.get(key)
        for key in ('attributes', 'conditions', 'optionsets')
    ):
        return {'attribute_map': {}}

    attribute_ids = set()
    question_ids = set()

    for element in elements:
        for descendant in get_element_descendants(element):
            if isinstance(descendant, (Page, QuestionSet, Question)) and descendant.attribute_id:
                attribute_ids.add(descendant.attribute_id)

            if isinstance(descendant, Question):
                question_ids.add(descendant.id)

            if isinstance(descendant, (Page, QuestionSet, Question)):
                attribute_ids.update(
                    condition.source_id
                    for condition in descendant.conditions.all()
                )

    if renderer_context.get('optionsets') and question_ids:
        attribute_ids.update(
            Condition.objects.filter(
                optionsets__questions__id__in=question_ids
            ).values_list('source_id', flat=True)
        )

    return {
        'attribute_map': Attribute.objects.get_queryset_ancestors(
            Attribute.objects.filter(id__in=attribute_ids),
            include_self=True
        ).in_bulk()
    }


def get_element_descendants(element):
    yield element
    yield from getattr(element, 'descendants', [])

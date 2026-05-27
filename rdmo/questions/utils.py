from rdmo.conditions.models import Condition
from rdmo.core.utils import is_truthy
from rdmo.domain.models import Attribute
from rdmo.questions.models import Page, Question, QuestionSet


def get_export_flags(request):
    full = is_truthy(request.GET.get('full'))
    return {
        'sections': full or is_truthy(request.GET.get('sections', True)),
        'pages': full or is_truthy(request.GET.get('pages', True)),
        'questionsets': full or is_truthy(request.GET.get('questionsets', True)),
        'questions': full or is_truthy(request.GET.get('questions', True)),
        'attributes': full or is_truthy(request.GET.get('attributes')),
        'optionsets': full or is_truthy(request.GET.get('optionsets')),
        'options': full or is_truthy(request.GET.get('options')),
        'conditions': full or is_truthy(request.GET.get('conditions')),
    }


def get_serializer_context(elements, export_flags):
    if not any(export_flags.get(key) for key in ('attributes', 'conditions', 'optionsets')):
        return export_flags

    attribute_ids = set()
    question_ids = set()

    for element in elements:
        for descendant in [element, *element.descendants]:
            if isinstance(descendant, (Page, QuestionSet, Question)) and descendant.attribute_id:
                attribute_ids.add(descendant.attribute_id)

            if isinstance(descendant, Question):
                question_ids.add(descendant.id)

            if isinstance(descendant, (Page, QuestionSet, Question)):
                attribute_ids.update(
                    condition.source_id
                    for condition in descendant.conditions.all()
                )

    if export_flags.get('optionsets') and question_ids:
        attribute_ids.update(
            Condition.objects.filter(
                optionsets__questions__id__in=question_ids
            ).values_list('source_id', flat=True)
        )

    return {
        **export_flags,
        'attribute_map': (
            Attribute.objects.get_queryset_ancestors(
                Attribute.objects.filter(id__in=attribute_ids),
                include_self=True
            ).in_bulk()
        )
    }

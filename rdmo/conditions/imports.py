import logging

from django.core.exceptions import ValidationError

from rdmo.core.xml import flat_xml_to_elements, filter_elements_by_type
from rdmo.domain.models import Attribute
from rdmo.options.models import Option

from .models import Condition
from .validators import ConditionUniqueKeyValidator

log = logging.getLogger(__name__)


def import_conditions(root):
    elements = flat_xml_to_elements(root)

    for element in filter_elements_by_type(elements, 'condition'):
        import_condition(element)


def import_condition(element):
    try:
        condition = Condition.objects.get(uri=element['uri'])
    except Condition.DoesNotExist:
        log.info('Condition not in db. Created with uri %s.', element['uri'])
        condition = Condition()

    condition.uri_prefix = element['uri_prefix'] or ''
    condition.key = element['key'] or ''
    condition.comment = element['comment'] or ''

    condition.source = None
    if element['source']:
        try:
            condition.source = Attribute.objects.get(uri=element['source'])
        except Attribute.DoesNotExist:
            pass

    condition.relation = element['relation']
    condition.target_text = element['target_text'] or ''

    condition.target_option = None
    if element['target_option']:
        try:
            condition.target_option = Option.objects.get(uri=element['target_option'])
        except Option.DoesNotExist:
            pass

    try:
        ConditionUniqueKeyValidator(condition).validate()
    except ValidationError as e:
        log.info('Condition not saving "%s" due to validation error (%s).', element['uri'], e)
        pass
    else:
        log.info('Condition saving to "%s".', element['uri'])
        condition.save()

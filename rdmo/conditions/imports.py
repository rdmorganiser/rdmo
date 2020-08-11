import logging

from rdmo.core.imports import (get_foreign_field, set_common_fields,
                               validate_instance)
from rdmo.domain.models import Attribute
from rdmo.options.models import Option

from .models import Condition

logger = logging.getLogger(__name__)


def import_condition(element, save=False):
    try:
        condition = Condition.objects.get(uri=element.get('uri'))
    except Condition.DoesNotExist:
        condition = Condition()

    set_common_fields(condition, element)

    condition.source = get_foreign_field(condition, element.get('source'), Attribute)
    condition.target_option = get_foreign_field(condition, element.get('target_option'), Option)

    condition.relation = element.get('relation')
    condition.target_text = element.get('target_text') or ''

    if save and validate_instance(condition):
        if condition.id:
            logger.info('Catalog created with uri %s.', element.get('uri'))
        else:
            logger.info('Catalog %s updated.', element.get('uri'))

        condition.save()
        condition.imported = True

    return condition

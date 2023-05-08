import logging

from rdmo.core.imports import (set_foreign_field, set_common_fields,
                               validate_instance)

from .models import Condition
from .validators import ConditionLockedValidator, ConditionUniqueURIValidator

logger = logging.getLogger(__name__)


def import_condition(element, save=False):
    try:
        condition = Condition.objects.get(uri=element.get('uri'))
    except Condition.DoesNotExist:
        condition = Condition()

    set_common_fields(condition, element)

    set_foreign_field(condition, 'source', element)
    set_foreign_field(condition, 'target_option', element)

    condition.relation = element.get('relation')
    condition.target_text = element.get('target_text') or ''

    if save and validate_instance(condition, ConditionLockedValidator, ConditionUniqueURIValidator):
        if condition.id:
            logger.info('Catalog created with uri %s.', element.get('uri'))
        else:
            logger.info('Catalog %s updated.', element.get('uri'))

        condition.save()
        condition.imported = True

    return condition

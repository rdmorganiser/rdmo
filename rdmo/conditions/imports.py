import logging

from rdmo.core.imports import (get_instance, set_common_fields,
                               set_foreign_field, set_temporary_fields,
                               validate_instance)
from rdmo.domain.models import Attribute
from rdmo.options.models import Option

from .models import Condition
from .validators import ConditionUniqueKeyValidator

logger = logging.getLogger(__name__)


def import_condition(element, save=[]):
    condition = get_instance(element, Condition)

    set_common_fields(condition, element)
    set_temporary_fields(condition, element)

    set_foreign_field(condition, 'source', element, Attribute)
    set_foreign_field(condition, 'target_option', element, Option)

    condition.relation = element.get('relation')
    condition.target_text = element.get('target_text') or ''

    validate_instance(condition, ConditionUniqueKeyValidator)

    if condition.uri in save:
        if condition.id:
            logger.info('Catalog created with uri %s.', element.get('uri'))
        else:
            logger.info('Catalog %s updated.', element.get('uri'))

        condition.save()

    return condition

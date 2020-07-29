import logging

from rdmo.core.imports import (get_instance, set_common_fields,
                               set_foreign_field, set_temporary_fields,
                               validate_instance)

from .models import Attribute
from .validators import AttributeUniquePathValidator

logger = logging.getLogger(__name__)


def import_attribute(element, save=[]):
    attribute = get_instance(element, Attribute)

    set_common_fields(attribute, element)
    set_temporary_fields(attribute, element)

    set_foreign_field(attribute, 'parent', element, Attribute)

    validate_instance(attribute, AttributeUniquePathValidator)

    if attribute.uri in save:
        if attribute.id:
            logger.debug('Attribute created with uri %s.', element.get('uri'))
        else:
            logger.debug('Attribute %s updated.', element.get('uri'))

        attribute.save()

    return attribute

import logging

from rdmo.core.imports import (set_common_fields, set_foreign_field,
                               validate_instance)

from .models import Attribute
from .validators import (AttributeLockedValidator, AttributeParentValidator,
                         AttributeUniqueURIValidator)

logger = logging.getLogger(__name__)


def import_attribute(element, save=False):
    try:
        attribute = Attribute.objects.get(uri=element.get('uri'))
    except Attribute.DoesNotExist:
        attribute = Attribute()

    set_common_fields(attribute, element)

    set_foreign_field(attribute, 'parent', element)

    if save and validate_instance(attribute,
                                  AttributeLockedValidator,
                                  AttributeParentValidator,
                                  AttributeUniqueURIValidator):
        if attribute.id:
            logger.debug('Attribute created with uri %s.', element.get('uri'))
        else:
            logger.debug('Attribute %s updated.', element.get('uri'))

        attribute.save()

    return attribute

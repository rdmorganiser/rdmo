import logging

from django.contrib.sites.models import Site

from rdmo.core.imports import check_permissions, set_common_fields, set_foreign_field, validate_instance

from .models import Attribute
from .validators import AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator

logger = logging.getLogger(__name__)


def import_attribute(element, save=False, user=None):
    try:
        attribute = Attribute.objects.get(uri=element.get('uri'))
    except Attribute.DoesNotExist:
        attribute = Attribute()

    set_common_fields(attribute, element)

    set_foreign_field(attribute, 'parent', element)

    attribute.path = Attribute.build_path(attribute.key, attribute.parent)

    validate_instance(attribute, element, AttributeLockedValidator,
                      AttributeParentValidator, AttributeUniqueURIValidator)

    check_permissions(attribute, element, user)

    if save and not element.get('errors'):
        if attribute.id:
            element['updated'] = True
            logger.debug('Attribute %s updated.', element.get('uri'))
        else:
            element['created'] = True
            logger.debug('Attribute created with uri %s.', element.get('uri'))

        attribute.save()
        attribute.editors.add(Site.objects.get_current())

    return attribute

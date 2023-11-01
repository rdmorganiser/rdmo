import copy
import logging

from django.contrib.sites.models import Site

from rdmo.core.imports import (
    check_diff_instance,
    check_permissions,
    set_common_fields,
    set_foreign_field,
    validate_instance,
)

from .models import Attribute
from .validators import AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator

logger = logging.getLogger(__name__)


def import_attribute(element, save=False, user=None):
    try:
        attribute = Attribute.objects.get(uri=element.get('uri'))
        original_attribute = copy.deepcopy(vars(attribute))
        element['updated'] = True
        _msg = 'Attribute %s updated.', element.get('uri')
    except Attribute.DoesNotExist:
        attribute = Attribute()
        element['created'] = True
        _msg = 'Attribute created with uri %s.', element.get('uri')

    set_common_fields(attribute, element)

    set_foreign_field(attribute, 'parent', element)

    attribute.path = Attribute.build_path(attribute.key, attribute.parent)

    validate_instance(attribute, element, AttributeLockedValidator,
                      AttributeParentValidator, AttributeUniqueURIValidator)

    check_permissions(attribute, element, user)

    if element.get('errors'):
        return attribute

    if element['updated']:

        diffs = check_diff_instance(original_attribute, element, check=True)
        if diffs:
            # breakpoint()
            diff_warning = "\n".join([f"{k}:{' '.join(val)}" for k, val in diffs.items()])
            element['diffs'] = diff_warning

    if save:
        attribute.save()
        attribute.editors.add(Site.objects.get_current())
        logger.debug(_msg)

    return attribute

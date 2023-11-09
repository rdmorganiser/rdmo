import logging

from django.contrib.sites.models import Site

from rdmo.core.imports import (
    check_permissions,
    get_or_return_instance,
    make_import_info_msg,
    set_common_fields,
    set_foreign_field,
    validate_instance,
)

from .models import Attribute
from .validators import AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator

logger = logging.getLogger(__name__)


def import_attribute(element, save=False, user=None):

    attribute, _created = get_or_return_instance(Attribute, uri=element.get('uri'))
    element['created'] = _created
    element['updated'] = not _created

    _msg = make_import_info_msg(attribute._meta.verbose_name, _created, uri=element.get('uri'))

    set_common_fields(attribute, element)

    set_foreign_field(attribute, 'parent', element)

    attribute.path = Attribute.build_path(attribute.key, attribute.parent)

    validate_instance(attribute, element, AttributeLockedValidator,
                      AttributeParentValidator, AttributeUniqueURIValidator)

    check_permissions(attribute, element, user)

    if element.get('errors'):
        return attribute

    if save:
        logger.debug(_msg)
        attribute.save()
        attribute.editors.add(Site.objects.get_current())

    return attribute

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

from .models import Condition
from .validators import ConditionLockedValidator, ConditionUniqueURIValidator

logger = logging.getLogger(__name__)


def import_condition(element, save=False, user=None):

    condition, _created = get_or_return_instance(Condition, uri=element.get('uri'))
    element['created'] = _created
    element['updated'] = not _created

    _msg = make_import_info_msg(condition._meta.verbose_name, _created, uri=element.get('uri'))

    set_common_fields(condition, element)

    set_foreign_field(condition, 'source', element)
    set_foreign_field(condition, 'target_option', element)

    condition.relation = element.get('relation')
    condition.target_text = element.get('target_text') or ''

    validate_instance(condition, element, ConditionLockedValidator, ConditionUniqueURIValidator)

    check_permissions(condition, element, user)

    if element.get('errors'):
        return condition

    if save:
        logger.info(_msg)
        condition.save()
        condition.editors.add(Site.objects.get_current())

    return condition

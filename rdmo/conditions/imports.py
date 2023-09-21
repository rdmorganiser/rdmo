import logging

from django.contrib.sites.models import Site

from rdmo.core.imports import check_permissions, set_common_fields, set_foreign_field, validate_instance

from .models import Condition
from .validators import ConditionLockedValidator, ConditionUniqueURIValidator

logger = logging.getLogger(__name__)


def import_condition(element, save=False, user=None):
    try:
        condition = Condition.objects.get(uri=element.get('uri'))
    except Condition.DoesNotExist:
        condition = Condition()

    set_common_fields(condition, element)

    set_foreign_field(condition, 'source', element)
    set_foreign_field(condition, 'target_option', element)

    condition.relation = element.get('relation')
    condition.target_text = element.get('target_text') or ''

    validate_instance(condition, element, ConditionLockedValidator, ConditionUniqueURIValidator)

    check_permissions(condition, element, user)

    if save and not element.get('errors'):
        if condition.id:
            element['updated'] = True
            logger.info('Condition %s updated.', element.get('uri'))
        else:
            element['created'] = True
            logger.info('Condition created with uri %s.', element.get('uri'))

        condition.save()
        condition.editors.add(Site.objects.get_current())

    return condition

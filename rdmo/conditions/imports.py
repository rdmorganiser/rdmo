import logging
from typing import Callable, Tuple

from django.contrib.sites.models import Site
from django.db import models

from rdmo.conditions.validators import ConditionLockedValidator, ConditionUniqueURIValidator
from rdmo.core.imports import (
    ElementImportHelper,
    check_permissions,
    set_foreign_field,
    validate_instance,
)

logger = logging.getLogger(__name__)


def import_condition(
        instance: models.Model,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
        user: models.Model = None
    ):

    set_foreign_field(instance, 'source', element)
    set_foreign_field(instance, 'target_option', element)

    instance.relation = element.get('relation')
    instance.target_text = element.get('target_text') or ''

    validate_instance(instance, element, *validators)

    check_permissions(instance, element, user)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        instance.editors.add(Site.objects.get_current())

    return instance


import_helper_condition = ElementImportHelper(
    model="conditions.condition",
    dotted_path='rdmo.conditions.models.Condition',
    import_method=import_condition,
    validators=(ConditionLockedValidator, ConditionUniqueURIValidator),
)

import logging
from typing import Callable, Tuple

from django.contrib.sites.models import Site

from rdmo.conditions.validators import ConditionLockedValidator, ConditionUniqueURIValidator
from rdmo.core.imports import (
    ElementImportHelper,
    validate_instance,
)

from .models import Condition

logger = logging.getLogger(__name__)


def import_condition(
        instance: Condition,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
    ):

    # set_foreign_field are already set in management/import.py
    # check_permissions already done in management/import.py
    instance.relation = element.get('relation') or ''
    instance.target_text = element.get('target_text') or ''

    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        instance.editors.add(Site.objects.get_current())

    return instance


import_helper_condition = ElementImportHelper(
    model="conditions.condition",
    import_func=import_condition,
    validators=(ConditionLockedValidator, ConditionUniqueURIValidator),
    lang_fields=[],
    foreign_fields=('source', 'target_option')
)

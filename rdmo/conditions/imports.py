import logging
from typing import Callable, Tuple

from rdmo.core.imports import (
    ElementImportHelper,
    validate_instance,
)

from .models import Condition
from .serializers.v1 import ConditionSerializer
from .validators import ConditionLockedValidator, ConditionUniqueURIValidator

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
        # sites and editors are added in management/import.py

    return instance


import_helper_condition = ElementImportHelper(
    model="conditions.condition",
    import_func=import_condition,
    validators=(ConditionLockedValidator, ConditionUniqueURIValidator),
    lang_fields=[],
    foreign_fields=('source', 'target_option'),
    serializer=ConditionSerializer
)

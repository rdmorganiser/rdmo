import logging
from typing import Callable, Tuple

from rdmo.core.imports import (
    ElementImportHelper,
    validate_instance,
)

from .models import Attribute
from .serializers.v1 import BaseAttributeSerializer
from .validators import AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator

logger = logging.getLogger(__name__)


def import_attribute(
    instance: Attribute, element: dict,
    validators: Tuple[Callable],
    save: bool = False) -> Attribute:

    # set_foreign_field are already set in management/import.py
    # check_permissions already done in management/import.py
    instance.path = instance.build_path(instance.key, instance.parent)
    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        # sites and editors are added in management/import.py

    return instance


import_helper_attribute = ElementImportHelper(
    model="domain.attribute",
    import_func=import_attribute,
    validators=(AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator),
    foreign_fields=('parent',),
    serializer=BaseAttributeSerializer,
)

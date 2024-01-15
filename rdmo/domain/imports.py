import logging
from typing import Callable, Tuple

from django.contrib.sites.models import Site

from rdmo.core.imports import (
    ElementImportHelper,
    validate_instance,
)
from rdmo.domain.validators import AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator

from .models import Attribute

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
        instance.editors.add(Site.objects.get_current())

    return instance


import_helper_attribute = ElementImportHelper(
    model="domain.attribute",
    import_method=import_attribute,
    validators=(AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator),
    lang_fields=[],
    foreign_fields=('parent',)
)

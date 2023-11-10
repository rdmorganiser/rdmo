import logging
from typing import Callable, Tuple

from django.contrib.sites.models import Site

from rdmo.core.imports import (
    check_permissions,
    set_foreign_field,
    validate_instance,
)

logger = logging.getLogger(__name__)


def import_attribute(instance, element, validators: Tuple[Callable], save=False, user=None):

    set_foreign_field(instance, 'parent', element)

    instance.path = instance.build_path(instance.key, instance.parent)

    validate_instance(instance, element, *validators)

    check_permissions(instance, element, user)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        instance.editors.add(Site.objects.get_current())

    return instance

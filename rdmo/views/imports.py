import logging
from typing import Callable, Tuple

from django.contrib.sites.models import Site
from django.db import models

from rdmo.core.imports import (
    check_permissions,
    set_lang_field,
    set_m2m_instances,
    validate_instance,
)

logger = logging.getLogger(__name__)


def import_view(
        instance: models.Model,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
        user: models.Model = None
    ):

    instance.order = element.get('order') or 0
    instance.template = element.get('template')

    set_lang_field(instance, 'title', element)
    set_lang_field(instance, 'help', element)

    instance.available = element.get('available', True)

    validate_instance(instance, element, *validators)

    check_permissions(instance, element, user)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_m2m_instances(instance, 'catalogs', element)
        instance.sites.add(Site.objects.get_current())
        instance.editors.add(Site.objects.get_current())

    return instance

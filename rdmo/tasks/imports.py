import logging
from typing import Callable, Tuple

from django.contrib.sites.models import Site
from django.db import models

from rdmo.core.imports import (
    ElementImportHelper,
    check_permissions,
    set_foreign_field,
    set_m2m_instances,
    validate_instance,
)
from rdmo.tasks.validators import TaskLockedValidator, TaskUniqueURIValidator

logger = logging.getLogger(__name__)


def import_task(
        instance: models.Model,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
        user: models.Model = None
    ):

    instance.order = element.get('order') or 0

    set_lang_field(instance, 'title', element)
    set_lang_field(instance, 'text', element)

    set_foreign_field(instance, 'start_attribute', element)
    set_foreign_field(instance, 'end_attribute', element)

    instance.days_before = element.get('days_before')
    instance.days_after = element.get('days_after')

    instance.available = element.get('available', True)

    validate_instance(instance, element, *validators)

    check_permissions(instance, element, user)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_m2m_instances(instance, 'catalogs', element)
        set_m2m_instances(instance, 'conditions', element)
        instance.sites.add(Site.objects.get_current())
        instance.editors.add(Site.objects.get_current())

    return instance


import_helper_task = ElementImportHelper(
    model="tasks.task",
    dotted_path="rdmo.tasks.models.Task",
    import_method=import_task,
    validators=(TaskLockedValidator, TaskUniqueURIValidator),
    lang_fields=('title', 'text')
)

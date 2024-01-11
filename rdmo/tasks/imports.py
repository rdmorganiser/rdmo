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

from .models import Task

logger = logging.getLogger(__name__)


def import_task(
        instance: Task,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
        user: models.Model = None
    ):
    # lang_fields are already set in management/import.py
    instance.order = element.get('order') or 0

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
    import_method=import_task,
    validators=(TaskLockedValidator, TaskUniqueURIValidator),
    lang_fields=('title', 'text')
)

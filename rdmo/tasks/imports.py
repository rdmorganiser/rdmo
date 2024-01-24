import logging
from typing import Callable, Tuple

from django.db import models

from rdmo.core.imports import (
    ElementImportHelper,
    set_m2m_instances,
    validate_instance,
)

from .models import Task
from .serializers.v1 import TaskSerializer
from .validators import TaskLockedValidator, TaskUniqueURIValidator

logger = logging.getLogger(__name__)


def import_task(
        instance: Task,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
        user: models.Model = None
    ):
    # lang_fields are already set in management/import.py
    # set_foreign_field are already set in management/import.py
    # check_permissions already done in management/import.py

    instance.order = element.get('order') or 0

    instance.days_before = element.get('days_before')
    instance.days_after = element.get('days_after')

    instance.available = element.get('available', True)

    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_m2m_instances(instance, 'catalogs', element)
        set_m2m_instances(instance, 'conditions', element)
        # sites and editors are added in management/import.py

    return instance


import_helper_task = ElementImportHelper(
    model="tasks.task",
    import_func=import_task,
    validators=(TaskLockedValidator, TaskUniqueURIValidator),
    lang_fields=('title', 'text'),
    foreign_fields=('start_attribute', 'end_attribute'),
    serializer=TaskSerializer
)

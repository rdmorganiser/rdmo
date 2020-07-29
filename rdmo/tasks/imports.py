import logging

from django.contrib.sites.models import Site
from rdmo.conditions.models import Condition
from rdmo.core.imports import (get_instance, get_m2m_instances,
                               set_common_fields, set_foreign_field,
                               set_lang_field, set_temporary_fields,
                               validate_instance)
from rdmo.domain.models import Attribute

from .models import Task
from .validators import TaskUniqueKeyValidator

logger = logging.getLogger(__name__)


def import_task(element, save=[]):
    task = get_instance(element, Task)

    set_common_fields(task, element)
    set_temporary_fields(task, element)

    set_lang_field(task, 'title', element)
    set_lang_field(task, 'text', element)

    set_foreign_field(task, 'start_attribute', element, Attribute)
    set_foreign_field(task, 'end_attribute', element, Attribute)

    task.days_before = element.get('days_before')
    task.days_after = element.get('days_after')

    conditions = get_m2m_instances(task, 'conditions', element, Condition)

    validate_instance(task, TaskUniqueKeyValidator)

    if task.uri in save:
        if task.id:
            logger.info('Task created with uri %s.', element.get('uri'))
        else:
            logger.info('Task %s updated.', element.get('uri'))

        task.save()
        task.sites.add(Site.objects.get_current())
        task.conditions.set(conditions)

    return task

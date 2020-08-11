import logging

from django.contrib.sites.models import Site

from rdmo.conditions.models import Condition
from rdmo.core.imports import (get_foreign_field, get_m2m_instances,
                               set_common_fields, set_lang_field,
                               validate_instance)
from rdmo.domain.models import Attribute

from .models import Task

logger = logging.getLogger(__name__)


def import_task(element, save=False):
    try:
        task = Task.objects.get(uri=element.get('uri'))
    except Task.DoesNotExist:
        task = Task()

    set_common_fields(task, element)

    set_lang_field(task, 'title', element)
    set_lang_field(task, 'text', element)

    task.start_attribute = get_foreign_field(task, element.get('start_attribute'), Attribute)
    task.end_attribute = get_foreign_field(task, element.get('end_attribute'), Attribute)

    task.days_before = element.get('days_before')
    task.days_after = element.get('days_after')

    conditions = get_m2m_instances(task, element.get('conditions'), Condition)

    if save and validate_instance(task):
        if task.id:
            logger.info('Task created with uri %s.', element.get('uri'))
        else:
            logger.info('Task %s updated.', element.get('uri'))

        task.save()
        task.sites.add(Site.objects.get_current())
        task.conditions.set(conditions)
        task.imported = True

    return task

import logging

from django.contrib.sites.models import Site

from rdmo.core.imports import (set_common_fields, set_foreign_field,
                               set_lang_field, set_m2m_instances,
                               validate_instance)

from .models import Task
from .validators import TaskLockedValidator, TaskUniqueURIValidator

logger = logging.getLogger(__name__)


def import_task(element, save=False):
    try:
        task = Task.objects.get(uri=element.get('uri'))
    except Task.DoesNotExist:
        task = Task()

    set_common_fields(task, element)

    set_lang_field(task, 'title', element)
    set_lang_field(task, 'text', element)

    set_foreign_field(task, 'start_attribute', element)
    set_foreign_field(task, 'end_attribute', element)

    task.days_before = element.get('days_before')
    task.days_after = element.get('days_after')

    task.available = element.get('available', True)

    validate_instance(task, element, TaskUniqueURIValidator, TaskLockedValidator)

    if save and not element.get('errors'):
        if task.id:
            element['updated'] = True
            logger.info('Task %s updated.', element.get('uri'))
        else:
            element['created'] = True
            logger.info('Task created with uri %s.', element.get('uri'))

        task.save()
        task.sites.add(Site.objects.get_current())
        set_m2m_instances(task, 'catalogs', element)
        set_m2m_instances(task, 'conditions', element)

    return task

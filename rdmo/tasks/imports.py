import logging

from django.contrib.sites.models import Site

from rdmo.core.imports import (set_common_fields, set_foreign_field,
                               set_lang_field, set_m2m_instances,
                               validate_instance)

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

    set_foreign_field(task, 'start_attribute', element)
    set_foreign_field(task, 'end_attribute', element)

    task.days_before = element.get('days_before')
    task.days_after = element.get('days_after')

    if save and validate_instance(task):
        if task.id:
            logger.info('Task created with uri %s.', element.get('uri'))
        else:
            logger.info('Task %s updated.', element.get('uri'))

        task.save()
        task.sites.add(Site.objects.get_current())
        set_m2m_instances(task, 'catalogs', element)
        set_m2m_instances(task, 'conditions', element)
        task.imported = True

    return task

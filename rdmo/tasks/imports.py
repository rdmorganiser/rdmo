import logging

from django.contrib.sites.models import Site

from rdmo.core.imports import (
    check_permissions,
    get_or_return_instance,
    make_import_info_msg,
    set_common_fields,
    set_foreign_field,
    set_lang_field,
    set_m2m_instances,
    validate_instance,
)

from .models import Task
from .validators import TaskLockedValidator, TaskUniqueURIValidator

logger = logging.getLogger(__name__)


def import_task(element, save=False, user=None):
    task, _created = get_or_return_instance(Task, uri=element.get('uri'))
    element['created'] = _created
    element['updated'] = not _created

    _msg = make_import_info_msg(task._meta.verbose_name, _created, uri=element.get('uri'))

    set_common_fields(task, element)

    task.order = element.get('order') or 0

    set_lang_field(task, 'title', element)
    set_lang_field(task, 'text', element)

    set_foreign_field(task, 'start_attribute', element)
    set_foreign_field(task, 'end_attribute', element)

    task.days_before = element.get('days_before')
    task.days_after = element.get('days_after')

    task.available = element.get('available', True)

    validate_instance(task, element, TaskUniqueURIValidator, TaskLockedValidator)

    check_permissions(task, element, user)

    if element.get('errors'):
        return task

    if save:
        logger.info(_msg)
        task.save()
        set_m2m_instances(task, 'catalogs', element)
        set_m2m_instances(task, 'conditions', element)
        task.sites.add(Site.objects.get_current())
        task.editors.add(Site.objects.get_current())

    return task

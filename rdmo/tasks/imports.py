import logging

from django.core.exceptions import ValidationError

from rdmo.core.xml import flat_xml_to_elements, filter_elements_by_type
from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute

from .models import Task
from .validators import TaskUniqueKeyValidator

log = logging.getLogger(__name__)


def import_tasks(root):
    elements = flat_xml_to_elements(root)

    for element in filter_elements_by_type(elements, 'task'):
        import_task(element)


def import_task(element):
    try:
        task = Task.objects.get(uri=element['uri'])
    except Task.DoesNotExist:
        log.info('Task not in db. Created with uri %s.', element['uri'])
        task = Task()

    task.uri_prefix = element['uri_prefix']
    task.key = element['key']
    task.comment = element['comment']

    task.title_en = element['title_en']
    task.title_de = element['title_de']
    task.text_en = element['text_en']
    task.text_de = element['text_de']

    if element['start_attribute']:
        try:
            task.start_attribute = Attribute.objects.get(uri=element['start_attribute'])
        except Attribute.DoesNotExist:
            pass

    if element['end_attribute']:
        try:
            task.end_attribute = Attribute.objects.get(uri=element['end_attribute'])
        except Attribute.DoesNotExist:
            pass

    task.days_before = element['days_before']
    task.days_after = element['days_after']

    try:
        TaskUniqueKeyValidator(task).validate()
    except ValidationError as e:
        log.info('Task not saving "%s" due to validation error (%s).', element['uri'], e)
        pass
    else:
        log.info('Task saving to "%s".', element['uri'])
        task.save()

    task.conditions.clear()
    if element['conditions'] is not None:
        for condition in element['conditions']:
            try:
                task.conditions.add(Condition.objects.get(uri=condition))
            except Condition.DoesNotExist:
                pass

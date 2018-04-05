import logging

from rdmo.core.utils import get_ns_map, get_uri, get_ns_tag
from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute
from rdmo.core.imports import get_value_from_treenode

from .models import Task, TimeFrame

log = logging.getLogger(__name__)


def import_tasks(tasks_node):
    log.info('Importing conditions')
    nsmap = get_ns_map(tasks_node.getroot())

    for task_node in tasks_node.findall('task'):
        task_uri = get_uri(task_node, nsmap)

        try:
            task = Task.objects.get(uri=task_uri)
        except Task.DoesNotExist:
            task = Task()
            log.info('Task not in db. Created with uri ' + task_uri)
        else:
            log.info('Task does exist. Loaded from uri ' + task_uri)

        task.uri_prefix = task_uri.split('/tasks/')[0]
        task.key = task_uri.split('/')[-1]

        try:
            attribute_uri = get_uri(task_node, nsmap, 'attrib')
            task.attribute = Attribute.objects.get(uri=attribute_uri)
        except (AttributeError, Attribute.DoesNotExist, KeyError):
            task.attribute = None

        for element in task_node.findall('title'):
            setattr(task, 'title_' + element.attrib['lang'], element.text)
        for element in task_node.findall('text'):
            setattr(task, 'text_' + element.attrib['lang'], element.text)

        log.info('Task saving to "' + str(task_uri) + '"')
        task.save()

        # TODO: finalize timeframe
        timeframe = TimeFrame()
        timeframe_node = task_node.find('timeframe')
        timeframe.start_attribute = timeframe_node.find('start_attribute').get(get_ns_tag('dc:uri', nsmap))
        timeframe.end_attribute = timeframe_node.find('end_attribute').get(get_ns_tag('dc:uri', nsmap))
        timeframe.days_before = get_value_from_treenode(timeframe_node, 'days_before')
        timeframe.days_after = get_value_from_treenode(timeframe_node, 'days_after')
        # log.info(nsmap)
        # log.info(str(start_attribute) + " - " + str(end_attribute) + " - " + str(days_before) + " - " + str(days_after))
        # timeframe.save()

        if hasattr(task_node, 'conditions'):
            for condition_node in task_node.find('condition').findall('conditions'):
                try:
                    condition_uri = get_uri(condition_node, nsmap)
                    condition = Condition.objects.get(uri=condition_uri)
                    task.conditions.add(condition)
                except Condition.DoesNotExist:
                    pass

from datetime import datetime, timedelta

from rdmo.core.utils import get_ns_tag
from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute

from .models import Task


def import_tasks(tasks_node):

    nsmap = tasks_node.nsmap

    for task_node in tasks_node.iterchildren():
        task_uri = task_node[get_ns_tag('dc:uri', nsmap)].text

        try:
            task = Task.objects.get(uri=task_uri)
        except Task.DoesNotExist:
            task = Task()

        task.uri_prefix = task_uri.split('/tasks/')[0]
        task.key = task_uri.split('/')[-1]

        try:
            attribute_uri = task_node['attribute'].get(get_ns_tag('dc:uri', nsmap))
            task.attribute = Attribute.objects.get(uri=attribute_uri)
        except (AttributeError, Attribute.DoesNotExist):
            task.attribute = None

        for element in task_node['title']:
            setattr(task, 'title_' + element.get('lang'), element.text)
        for element in task_node['text']:
            setattr(task, 'text_' + element.get('lang'), element.text)

        task.save()

        if hasattr(task_node, 'conditions'):
            for condition_node in task_node.conditions.iterchildren():
                try:
                    condition_uri = condition_node.get(get_ns_tag('dc:uri', nsmap))
                    condition = Condition.objects.get(uri=condition_uri)
                    task.conditions.add(condition)
                except Condition.DoesNotExist:
                    pass

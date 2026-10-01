from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute
from rdmo.options.models import Option

from ..models import Task

URI_PREFIX = 'https://example.com/terms'


def create_tasks_with_conditions(count, uri_path):
    """Create tasks sharing attributes and conditions with distinct target options."""
    attributes = {
        name: Attribute.objects.create(
            uri_prefix=URI_PREFIX,
            key=f'{uri_path}-{name}',
        )
        for name in ('start', 'end', 'source')
    }

    conditions = []
    for index in range(3):
        option = Option.objects.create(
            uri_prefix=URI_PREFIX,
            uri_path=f'{uri_path}-option-{index:04d}',
            text_lang1=f'Export option {index}',
        )
        condition = Condition.objects.create(
            uri_prefix=URI_PREFIX,
            uri_path=f'{uri_path}-condition-{index:04d}',
            source=attributes['source'],
            relation=Condition.RELATION_EQUAL,
            target_option=option,
        )
        conditions.append(condition)

    tasks = []
    for index in range(count):
        task = Task.objects.create(
            uri_prefix=URI_PREFIX,
            uri_path=f'{uri_path}-{index:04d}',
            title_lang1=f'Export task {index}',
            start_attribute=attributes['start'],
            end_attribute=attributes['end'],
        )
        task.conditions.add(*conditions)
        tasks.append(task)

    return tasks, attributes, conditions

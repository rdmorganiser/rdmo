import iso8601

from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.simple_tag(takes_context=True)
def task_deadline(context, project, task):

    try:
        value = project.current_snapshot.values.all().get(attribute=task.attribute)
    except ObjectDoesNotExist:
        return ''

    try:
        return iso8601.parse_date(value.text) + task.time_period
    except iso8601.ParseError:
        return ''

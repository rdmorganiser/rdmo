from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from ..utils import get_full_name

register = template.Library()


@register.simple_tag()
def full_name(user):
    return get_full_name(user)


@register.simple_tag()
def user_data_as_dl(user):
    html = '<dl>'
    html += '<dt>{key}</dt><dd>{value}</dd>'.format(
        key=_('Name'),
        value=get_full_name(user),
    )
    for additional_value in user.additional_values.all():
        html += f'<dt>{additional_value.field.text}</dt><dd>{additional_value.value}</dd>'
    html += '</dl>'
    return mark_safe(html)

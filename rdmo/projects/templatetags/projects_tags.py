from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from ..models import Membership

register = template.Library()


@register.simple_tag()
def projects_indent(level):
    string = ''
    if level > 0:
        for _ in range(level - 1):
            string += '&ensp;&ensp;'
        string += '&#8226;&ensp;'

    return mark_safe('<span class="projects-indent">' + string + '</span>')


@register.filter()
@stringfilter
def projects_role(role):
    return dict(Membership.ROLE_CHOICES).get(role, '')

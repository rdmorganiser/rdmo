from django import template
from django.template.loader import render_to_string

from ..utils import get_values_tree

register = template.Library()

@register.simple_tag(takes_context=True)
def values_tree(context, **kwargs):

    tree = get_values_tree(context['project'])

    return render_to_string('projects/values_tree.html', {'values_tree': tree})

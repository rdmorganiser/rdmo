from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag()
def ng_form_field(field_type, label, field, options=None):

    template_name = 'core/ng_form_field_%s.html' % field_type
    ng_model = 'service.values.%s' % field
    ng_errors = 'service.errors.%s' % field

    return render_to_string(template_name, {
        'label': label,
        'field': field,
        'ng_model': ng_model,
        'ng_errors': ng_errors,
        'options': options
    })

from django import template
from django.utils.translation import gettext_lazy as _

from rdmo.core.constants import VALUE_TYPE_DATETIME, VALUE_TYPE_INTEGER, VALUE_TYPE_TEXT
from rdmo.projects.models import Value

register = template.Library()


@register.simple_tag(takes_context=True)
def get_values(context, attribute, set_prefix='*', set_index='*', index='*', project=None):
    if project is None:
        project = context['project']

    if attribute == 'project/id':
        return [Value(text=project.id, value_type=VALUE_TYPE_INTEGER).as_dict]
    elif attribute == 'project/title':
        return [Value(text=project.title, value_type=VALUE_TYPE_TEXT).as_dict]
    elif attribute == 'project/description':
        return [Value(text=project.description, value_type=VALUE_TYPE_TEXT).as_dict]
    elif attribute == 'project/created':
        return [Value(text=project.created, value_type=VALUE_TYPE_DATETIME).as_dict]
    elif attribute == 'project/updated':
        return [Value(text=project.updated, value_type=VALUE_TYPE_DATETIME).as_dict]
    if attribute == 'project/snapshot/id':
        return [Value(text=project.snapshot.get('id'), value_type=VALUE_TYPE_INTEGER).as_dict]
    elif attribute == 'project/snapshot/title':
        return [Value(text=project.snapshot.get('title'), value_type=VALUE_TYPE_TEXT).as_dict]
    elif attribute == 'project/snapshot/description':
        return [Value(text=project.snapshot.get('description'), value_type=VALUE_TYPE_TEXT).as_dict]
    elif attribute == 'project/snapshot/created':
        return [Value(text=project.snapshot.get('created'), value_type=VALUE_TYPE_DATETIME).as_dict]
    elif attribute == 'project/snapshot/updated':
        return [Value(text=project.snapshot.get('updated'), value_type=VALUE_TYPE_DATETIME).as_dict]
    else:
        return project._get_values(attribute, set_prefix, set_index, index)


@register.simple_tag(takes_context=True)
def get_numbers(context, attribute, set_prefix='*', set_index='*', index='*', project=None):
    values = get_values(context, attribute, set_prefix, set_index, index, project)
    return [value.get('as_number', 0) for value in values]


@register.simple_tag(takes_context=True)
def get_value(context, attribute, set_prefix='', set_index=0, index=0, project=None):
    try:
        return get_values(context, attribute, set_prefix=set_prefix, set_index=set_index,
                          index=index, project=project)[0]
    except IndexError:
        return None


@register.simple_tag(takes_context=True)
def get_number(context, attribute, set_prefix='', set_index=0, index=0, project=None):
    value = get_value(context, attribute, set_prefix, set_index, index, project)
    if value is None:
        return 0
    else:
        return value.get('as_number', 0)


@register.simple_tag(takes_context=True)
def get_set_values(context, set, attribute, set_prefix='', project=None):
    set_index = set.get('set_index')
    return get_values(context, attribute, set_prefix=set_prefix, set_index=set_index, project=project)


@register.simple_tag(takes_context=True)
def get_set_value(context, set, attribute, set_prefix='', index=0, project=None):
    try:
        set_index = set.get('set_index')
        return get_values(context, attribute, set_prefix=set_prefix, set_index=set_index,
                          index=index, project=project)[0]
    except IndexError:
        return None


@register.simple_tag(takes_context=True)
def get_set_prefixes(context, attribute, project=None):
    try:
        return sorted({value['set_prefix'] for value in get_values(context, attribute, project=project)})
    except IndexError:
        return None


@register.simple_tag(takes_context=True)
def get_set_indexes(context, attribute, set_prefix='', project=None):
    try:
        return sorted({
            value['set_index'] for value in get_values(context, attribute, set_prefix=set_prefix, project=project)
        })
    except IndexError:
        return None


@register.simple_tag(takes_context=True)
def get_sets(context, attribute, set_prefix='', project=None):
    # get the values for the set attribute
    values = get_values(context, attribute.rstrip('/'), set_prefix=set_prefix, index=0, project=project)
    if values:
        return values
    elif not attribute.endswith('/id'):
        # for backwards compatibility, try again with the /id attribute
        return get_sets(context, attribute.rstrip('/') + '/id', set_prefix=set_prefix, project=project)


@register.simple_tag(takes_context=True)
def get_set(context, attribute, set_prefix='', project=None):
    # for backwards compatibility, identical to get_sets
    return get_sets(context, attribute, set_prefix=set_prefix, project=project)


@register.inclusion_tag('views/tags/value.html', takes_context=True)
def render_value(context, attribute, set_prefix='', set_index=0, index=0, project=None):
    context['value'] = get_value(context, attribute, set_prefix=set_prefix, set_index=set_index,
                                 index=index, project=project)
    return context


@register.inclusion_tag('views/tags/value_list.html', takes_context=True)
def render_value_list(context, attribute, set_prefix='', set_index=0, project=None):
    context['values'] = get_values(context, attribute, set_prefix=set_prefix, set_index=set_index, project=project)
    return context


@register.inclusion_tag('views/tags/value_inline_list.html', takes_context=True)
def render_value_inline_list(context, attribute, set_prefix='', set_index=0, project=None):
    context['values'] = get_values(context, attribute, set_prefix=set_prefix, set_index=set_index, project=project)
    return context


@register.inclusion_tag('views/tags/value.html', takes_context=True)
def render_set_value(context, set, attribute, set_prefix='', index=0, project=None):
    context['value'] = get_set_value(context, set, attribute, set_prefix=set_prefix, index=index, project=project)
    return context


@register.inclusion_tag('views/tags/value_list.html', takes_context=True)
def render_set_value_list(context, set, attribute, set_prefix='', project=None):
    context['values'] = get_set_values(context, set, attribute, set_prefix=set_prefix, project=project)
    return context


@register.inclusion_tag('views/tags/value_inline_list.html', takes_context=True)
def render_set_value_inline_list(context, set, attribute, set_prefix='', project=None):
    context['values'] = get_set_values(context, set, attribute, set_prefix=set_prefix, project=project)
    return context


@register.simple_tag(takes_context=True)
def check_element(context, element, set_prefix=None, set_index=None, project=None):
    if project is None:
        project = context['project']

    return project._check_element(element, set_prefix=None, set_index=None)


@register.simple_tag(takes_context=True)
def check_condition(context, condition, set_prefix=None, set_index=None, project=None):
    if project is None:
        project = context['project']

    return project._check_condition(condition, set_prefix=None, set_index=None)


@register.simple_tag(takes_context=True)
def get_labels(context, element, set_prefix='', set_index=0, project=None):
    if project is None:
        project = context['project']

    set_labels = []
    for ancestor in element['ancestors']:
        if ancestor['is_collection']:
            set_label = f'#{set_index + 1}'

            if ancestor['attribute']:
                # get attribute value
                value = get_value(context, ancestor['attribute'], set_prefix=set_prefix, set_index=set_index,
                                  index=0, project=project)
                if value:
                    set_label = '"{}"'.format(value['value'])

            set_labels.append('{} {}'.format(ancestor['verbose_name'].title() or _('Set'), set_label))

            if set_prefix != '':
                rpartition = set_prefix.rpartition('|')
                set_prefix, set_index = rpartition[0], int(rpartition[2])

    # flip the list
    set_labels.reverse()

    return set_labels


@register.filter
def is_true(values):
    return [value for value in values if value['is_true']]


@register.filter
def is_false(values):
    return [value for value in values if value['is_false']]


@register.filter
def is_empty(values):
    return [value for value in values if value['is_empty']]


@register.filter
def is_not_empty(values):
    return [value for value in values if not value['is_empty']]

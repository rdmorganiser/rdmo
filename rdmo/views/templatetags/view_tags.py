from urllib.parse import urlparse

from django import template

from rdmo.core.constants import (VALUE_TYPE_DATETIME, VALUE_TYPE_INTEGER,
                                 VALUE_TYPE_TEXT)

register = template.Library()


@register.simple_tag(takes_context=True)
def get_values(context, attribute, set_index='*', index='*', project_id=None):
    from rdmo.projects.models import Project, Value

    if project_id:
        # check if the project_id is in project_descendants
        if project_id not in context['project_descendants']:
            return Value.objects.none()

        snapshot_id = None
    else:
        project_id = context['project_id']
        snapshot_id = context['snapshot_id']

    # get the project
    project = Project.objects.get(id=project_id)

    if attribute == 'project/id':
        return [Value(text=project.id, value_type=VALUE_TYPE_INTEGER)]
    elif attribute == 'project/title':
        return [Value(text=project.title, value_type=VALUE_TYPE_TEXT)]
    elif attribute == 'project/description':
        return [Value(text=project.description, value_type=VALUE_TYPE_TEXT)]
    elif attribute == 'project/created':
        return [Value(text=project.created, value_type=VALUE_TYPE_DATETIME)]
    elif attribute == 'project/updated':
        return [Value(text=project.updated, value_type=VALUE_TYPE_DATETIME)]
    else:
        queryset = project.values.filter(snapshot_id=snapshot_id)

        if urlparse(attribute).scheme:
            queryset = queryset.filter(attribute__uri=attribute)
        else:
            queryset = queryset.filter(attribute__path=attribute)

        if set_index != '*':
            queryset = queryset.filter(set_index=set_index)

        if index != '*':
            queryset = queryset.filter(collection_index=index)

        return queryset.order_by('set_index').order_by('collection_index')


@register.simple_tag(takes_context=True)
def get_value(context, attribute, set_index=0, index=0, project_id=None):
    try:
        return get_values(context, attribute, set_index, index, project_id)[0]
    except IndexError:
        return None


@register.simple_tag(takes_context=True)
def get_set_values(context, set, attribute, index='*', project_id=None):
    return get_values(context, attribute, set.set_index, index, project_id)


@register.simple_tag(takes_context=True)
def get_set_value(context, set, attribute, index=0, project_id=None):
    try:
        return get_values(context, attribute, set.set_index, index, project_id)[0]
    except IndexError:
        return None


@register.simple_tag(takes_context=True)
def get_sets(context, attribute, project_id=None):
    return get_values(context, attribute.rstrip('/') + '/id', index=0, project_id=project_id)


@register.simple_tag(takes_context=True)
def get_set(context, attribute, project_id=None):
    # for backwards compatibility, identical to get_sets
    return get_sets(context, attribute, project_id)


@register.inclusion_tag('views/tags/value.html', takes_context=True)
def render_value(context, attribute, set_index=0, index=0, project_id=None):
    context['value'] = get_value(context, attribute, set_index, index, project_id)
    return context


@register.inclusion_tag('views/tags/value_list.html', takes_context=True)
def render_value_list(context, attribute, set_index=0, project_id=None):
    context['values'] = get_values(context, attribute, set_index, project_id)
    return context


@register.inclusion_tag('views/tags/value_inline_list.html', takes_context=True)
def render_value_inline_list(context, attribute, set_index=0, project_id=None):
    context['values'] = get_values(context, attribute, set_index, project_id)
    return context


@register.inclusion_tag('views/tags/value.html', takes_context=True)
def render_set_value(context, set, attribute, index=0, project_id=None):
    context['value'] = get_set_value(context, set, attribute, index, project_id)
    return context


@register.inclusion_tag('views/tags/value_list.html', takes_context=True)
def render_set_value_list(context, set, attribute, project_id=None):
    context['values'] = get_set_values(context, set, attribute, project_id)
    return context


@register.inclusion_tag('views/tags/value_inline_list.html', takes_context=True)
def render_set_value_inline_list(context, set, attribute, project_id=None):
    context['values'] = get_set_values(context, set, attribute, project_id)
    return context

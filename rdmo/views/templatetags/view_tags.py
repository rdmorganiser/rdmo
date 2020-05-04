from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_values(context, attribute_path, set_index='*', index='*'):
    if set_index == '*' and index == '*':
        try:
            return context['values'][attribute_path]
        except KeyError:
            return []

    elif set_index == '*':
        try:
            value_sets = context['values'][attribute_path]
        except KeyError:
            return []

        values = []
        for value_set in value_sets:
            try:
                values.append(value_set[index])
            except IndexError:
                values.append('')
        values = sorted(values, reverse=False, key=lambda x: x.id)
        return values

    elif index == '*':
        try:
            return context['values'][attribute_path][set_index]
        except (KeyError, IndexError):
            return []
    else:
        try:
            return context['values'][attribute_path][set_index][index]
        except (KeyError, IndexError):
            return ''


@register.simple_tag(takes_context=True)
def get_set_values(context, set, attribute_path, index='*'):
    return get_values(context, attribute_path, set.set_index, index)

@register.simple_tag(takes_context=True)
def get_value(context, attribute_path, set_index=0, index=0):
    return get_values(context, attribute_path, set_index, index)

@register.simple_tag(takes_context=True)
def get_set_value(context, set, attribute_path, index=0):
    return get_set_values(context, set, attribute_path, index)

@register.simple_tag(takes_context=True)
def get_set(context, attribute_path):
    id_path = attribute_path.rstrip('/') + '/id'
    return get_values(context, id_path, index=0)


@register.inclusion_tag('views/tags/value.html', takes_context=True)
def render_value(context, attribute_path, set_index=0, index=0):
    try:
        return {'value': get_values(context, attribute_path, set_index, index)}
    except KeyError:
        return None


@register.inclusion_tag('views/tags/value.html', takes_context=True)
def render_set_value(context, set, attribute_path, index=0):
    try:
        return {'value': get_values(context, attribute_path, set.set_index, index)}
    except KeyError:
        return None


@register.inclusion_tag('views/tags/value_list.html', takes_context=True)
def render_value_list(context, attribute_path, set_index=0):
    try:
        return {'values': get_values(context, attribute_path, set_index)}
    except KeyError:
        return None


@register.inclusion_tag('views/tags/value_list.html', takes_context=True)
def render_set_value_list(context, set, attribute_path):
    try:
        return {'values': get_values(context, attribute_path, set.set_index)}
    except KeyError:
        return None


@register.inclusion_tag('views/tags/value_inline_list.html', takes_context=True)
def render_value_inline_list(context, attribute_path, set_index=0):
    try:
        return {'values': get_values(context, attribute_path, set_index)}
    except KeyError:
        return None


@register.inclusion_tag('views/tags/value_inline_list.html', takes_context=True)
def render_set_value_inline_list(context, set, attribute_path):
    try:
        return {'values': get_values(context, attribute_path, set.set_index)}
    except KeyError:
        return None

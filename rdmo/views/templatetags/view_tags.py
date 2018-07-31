from django import template

register = template.Library()


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
def values(context, attribute_path, set_index='*', index='*'):
    try:
        return get_values(context, attribute_path, set_index, index)
    except KeyError:
        return None


@register.simple_tag(takes_context=True)
def sets(context, attribute_path):
    try:
        return get_values(context, attribute_path, index=0)
    except KeyError:
        return None


@register.inclusion_tag('views/tags/value.html', takes_context=True)
def value(context, attribute_path, set_index=0, index=0):
    try:
        return {'value': get_values(context, attribute_path, set_index, index)}
    except KeyError:
        return None


@register.inclusion_tag('views/tags/value_list.html', takes_context=True)
def value_list(context, attribute_path, set_index=0):
    try:
        return {'values': get_values(context, attribute_path, set_index)}
    except KeyError:
        return None

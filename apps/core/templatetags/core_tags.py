from django import template
from django.conf import settings
from django.utils import translation
from django.core.urlresolvers import reverse

from ..utils import get_internal_link

register = template.Library()


@register.simple_tag(takes_context=True)
def internal_link(context, text, name, *args, **kwargs):
    if 'permission' in kwargs:
        if kwargs['permission'] == 'login_required':
            if not context.request.user.is_authenticated():
                return ''
        else:
            if not context.request.user.has_perm(kwargs['permission']):
                return ''
        del kwargs['permission']

    return get_internal_link(text, name, *args, **kwargs)


@register.simple_tag(takes_context=True)
def admin_link(context):
    if not context.request.user.is_superuser:
        return ''

    return get_internal_link('Admin', 'admin:index')


@register.simple_tag(takes_context=True)
def login_link(context):
    if context.request.user.is_authenticated():
        return get_internal_link('Logout', 'logout')
    else:
        return get_internal_link('Login', 'login')


@register.simple_tag()
def i18n_switcher():
    string = ''
    for language, language_string in settings.LANGUAGES:
        url = reverse('i18n_switcher', args=[language])
        if language == translation.get_language():
            string += "<li><a href=\"%s\"><u>%s</u></a></li>" % (url, language_string)
        else:
            string += "<li><a href=\"%s\">%s</a></li>" % (url, language_string)

    return string

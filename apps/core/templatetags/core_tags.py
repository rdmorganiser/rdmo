from django import template
from django.conf import settings
from django.utils import translation
from django.core.urlresolvers import reverse

from ..utils import get_internal_link

register = template.Library()


@register.simple_tag(takes_context=True)
def internal_link(context, name, text=None, permission=None):
    if permission:
        if permission == 'login_required':
            if not context.request.user.is_authenticated():
                return ''
        else:
            if not context.request.user.has_perm(permission):
                return ''

    return get_internal_link(name, text)


@register.simple_tag(takes_context=True)
def admin_link(context, text='Admin'):
    if not context.request.user.is_superuser:
        return ''

    return get_internal_link('admin:index', text)


@register.simple_tag(takes_context=True)
def login_link(context):
    if context.request.user.is_authenticated():
        return get_internal_link('logout', 'Logout')
    else:
        return get_internal_link('login', 'Login')


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

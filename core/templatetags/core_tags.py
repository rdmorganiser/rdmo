from django import template
from django.conf import settings
from django.utils import translation
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag()
def internal_link(name, text=None, style=None):
    url = reverse(name)

    if text is None:
        text = url

    return "<a href=\"%s\">%s</a>" % (url, text)


@register.simple_tag(takes_context=True)
def login_link(context):
    if context.request.user.is_authenticated():
        return internal_link('logout', 'Logout')
    else:
        return internal_link('login', 'Login')


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


@register.simple_tag()
def full_name(user):
    if hasattr(user, 'first_name') and hasattr(user, 'last_name') and user.first_name and user.last_name:
        return '%s %s' % (user.first_name, user.last_name)
    else:
        return user.username

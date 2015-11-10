from django import template
from django.conf import settings
from django.utils import translation
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def login_link(context):
    if context.request.user.is_authenticated():
        url = reverse('logout')
        text = 'Logout'
    else:
        url = reverse('login')
        text = 'Login'

    return "<a href=\"%s\">%s</a>" % (url, text)


@register.simple_tag()
def internal_link(name, text=None):
    url = reverse(name)

    if text is None:
        text = url
    return "<a href=\"%s\">%s</a>" % (url, text)


@register.simple_tag()
def i18n_switcher():
    string = ''
    for language in settings.LANGUAGES:
        if language[0] == translation.get_language():
            string += "<li><a class="" href=\"/i18n/%s\"><u>%s</u></a></li>" % language
        else:
            string += "<li><a href=\"/i18n/%s\">%s</a></li>" % language

    return string

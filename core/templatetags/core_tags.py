from django import template
from django.conf import settings
from django.utils import translation
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

register = template.Library()


@register.simple_tag()
def base_url():
    path = '/'.join(Site.objects.get_current().domain.rstrip('/').split('/')[1:])
    if path:
        path = '/' + path
    return path


@register.simple_tag()
def internal_link(name, text=None, style=None):
    url = reverse(name)

    if text is None:
        text = url

    return "<a href=\"%s%s\">%s</a>" % (base_url(), url, text)


@register.simple_tag(takes_context=True)
def login_link(context):
    if context.request.user.is_authenticated():
        return internal_link('logout', 'Logout')
    else:
        return internal_link('login', 'Login')


@register.simple_tag()
def i18n_switcher():
    base = base_url() + '/i18n/'
    string = ''
    for language, language_string in settings.LANGUAGES:
        if language == translation.get_language():
            string += "<li><a href=\"%s%s\"><u>%s</u></a></li>" % (base, language, language_string)
        else:
            string += "<li><a href=\"%s%s\">%s</a></li>" % (base, language, language_string)

    return string


@register.simple_tag()
def full_name(user):
    if hasattr(user, 'first_name') and hasattr(user, 'last_name') and user.first_name and user.last_name:
        return '%s %s' % (user.first_name, user.last_name)
    else:
        return user.username

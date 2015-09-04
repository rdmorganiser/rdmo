from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def login_link(context):
    if context.request.user.is_authenticated():
        url = settings.LOGOUT_URL
        text = 'Logout'
    else:
        url = settings.LOGIN_URL
        text = 'Login'

    return "<a href=\"%s\">%s</a>" % (url,text)

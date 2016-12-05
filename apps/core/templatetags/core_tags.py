from markdown import markdown as markdown_function

from django import template
from django.conf import settings
from django.utils import translation
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def login_url():
    return settings.LOGIN_URL


@register.simple_tag()
def logout_url():
    return settings.LOGOUT_URL


@register.simple_tag()
def i18n_switcher():
    string = ''
    for language, language_string in settings.LANGUAGES:
        url = reverse('i18n_switcher', args=[language])
        if language == translation.get_language():
            string += "<li><a href=\"%s\"><u>%s</u></a></li>" % (url, language_string)
        else:
            string += "<li><a href=\"%s\">%s</a></li>" % (url, language_string)

    return mark_safe(string)


@register.simple_tag(takes_context=True)
def bootstrap_form(context, **kwargs):
    form_context = {}

    if 'form' in kwargs:
        form_context['form'] = kwargs['form']
    else:
        form_context['form'] = context['form']

    if 'next' in kwargs:
        form_context['next'] = kwargs['next']
    elif 'next' in context:
        form_context['next'] = context['next']

    if 'action_url_name' in kwargs:
        form_context['action'] = reverse(kwargs['action_url_name'])

    if 'submit' in kwargs:
        form_context['submit'] = kwargs['submit']

    return render_to_string('core/bootstrap_form.html', form_context, request=context.request)


@register.simple_tag(takes_context=True)
def bootstrap_delete_form(context, **kwargs):
    form_context = {}

    if 'next' in kwargs:
        form_context['next'] = kwargs['next']
    elif 'next' in context:
        form_context['next'] = context['next']

    if 'action_url_name' in kwargs:
        form_context['action'] = reverse(kwargs['action_url_name'])

    if 'submit' in kwargs:
        form_context['submit'] = kwargs['submit']

    return render_to_string('core/bootstrap_delete_form.html', form_context, request=context.request)


@register.filter(name='next')
def next(value, arg):
    try:
        return value[int(arg)+1]
    except:
        return None


@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    return mark_safe(markdown_function(force_text(value)))

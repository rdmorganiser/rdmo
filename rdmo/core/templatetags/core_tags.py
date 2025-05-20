from django import template
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.defaultfilters import stringfilter
from django.template.loader import get_template, render_to_string
from django.urls import resolve, reverse
from django.urls.resolvers import Resolver404
from django.utils import translation
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, to_locale

from rdmo import __version__
from rdmo.core.utils import markdown2html, remove_html_special_characters

register = template.Library()


@register.simple_tag()
def i18n_switcher():
    string = ''
    for language, language_string in settings.LANGUAGES:
        url = reverse('i18n_switcher', args=[language])
        if language == translation.get_language():
            string += f"<li><a class=\"dropdown-item\" href=\"{url}\"><u>{language_string}</u></a></li>"
        else:
            string += f"<li><a class=\"dropdown-item\" href=\"{url}\">{language_string}</a></li>"
    return mark_safe(string)


@register.simple_tag()
def render_lang_template(template_name, escape_html=False):
    loc = to_locale(get_language())
    lst = [
        template_name + '_' + loc + '.html',
        template_name + '_' + settings.LANGUAGES[0][0] + '.html',
        template_name + '_en.html',
        template_name + '.html'
    ]
    for el in lst:
        try:
            template = get_template(el)
            html = template.render()
            if escape_html:
                return escape(html)
            else:
                return html
        except TemplateDoesNotExist:
            pass
    return ''


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

    if 'delete' in kwargs:
        form_context['delete'] = kwargs['delete']

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


@register.simple_tag(takes_context=True)
def back_to_project_link(context):
    try:
        resolver_match = resolve(context.request.path_info)
        if resolver_match.url_name != 'project':
            project = context.get('project')
            if project:
                project_id = project.id
            else:
                project_id = resolver_match.kwargs.get('project_id')

            if project_id is not None:
                return render_to_string('core/back_to_project_link.html', {
                    'project_id': project_id
                }, request=context.request)
    except Resolver404:
        pass

    return ''


@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    return mark_safe(markdown2html(value))


@register.simple_tag
def version():
    return __version__


@register.filter('startswith')
@stringfilter
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter()
@stringfilter
def clean(string):
    return remove_html_special_characters(string)

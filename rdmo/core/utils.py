import importlib
import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.template.loader import get_template, render_to_string
from django.utils.dateparse import parse_date
from django.utils.encoding import force_str
from django.utils.formats import get_format
from django.utils.translation import gettext_lazy as _

from defusedcsv import csv
from markdown import markdown

from .constants import HUMAN2BYTES_MAPPER
from .pandoc import get_pandoc_content, get_pandoc_content_disposition

log = logging.getLogger(__name__)


def get_script_alias(request):
    return request.path[:-len(request.path_info)]


def get_referer(request, default=None):
    return request.META.get('HTTP_REFERER', default)


def get_referer_path_info(request, default=''):
    referer = request.META.get('HTTP_REFERER', None)
    if not referer:
        return default

    script_alias = get_script_alias(request)
    return urlparse(referer).path[len(script_alias):]


def get_next(request):
    next = request.POST.get('next')
    current = request.path_info

    if next in (current, None):
        return get_script_alias(request) + '/'
    else:
        return get_script_alias(request) + next


def get_uri_prefix(obj):
    # needs to stay, is part of a migration
    r = settings.DEFAULT_URI_PREFIX
    if bool(obj.uri_prefix) is True:
        r = obj.uri_prefix.rstrip('/')
    return r


def join_url(base, *args) -> str:
    url = base
    for arg in args:
        url = url.rstrip('/') + '/' + arg.lstrip('/')
    return url


def get_model_field_meta(model):
    meta = {}

    for field in model._meta.get_fields():
        match = re.search(r'lang(\d)$', field.name)
        if match:
            lang_index = int(match.group(1))

            try:
                lang_code, lang = settings.LANGUAGES[lang_index - 1]
            except IndexError:
                continue

            field_name = field.name.replace(f'_lang{lang_index}', f'_{lang_code}')

            meta[field_name] = {}
            if hasattr(field, 'verbose_name'):
                # remove the "(primary)" part
                meta[field_name]['verbose_name'] = re.sub(r'\(.*\)$', f'({lang})', str(field.verbose_name))
            if hasattr(field, 'help_text'):
                # remove the "in the primary language" part
                meta[field_name]['help_text'] = re.sub(r' \(.*\).', '.', str(field.help_text))
        else:
            meta[field.name] = {}
            if hasattr(field, 'verbose_name'):
                meta[field.name]['verbose_name'] = field.verbose_name
            if hasattr(field, 'help_text'):
                meta[field.name]['help_text'] = field.help_text

    if model.__name__ == 'Page':
        meta['elements'] = {
            'verbose_name': _('Elements'),
            'help_text': _('The questions and question sets for this page.')
        }
    elif model.__name__ == 'QuestionSet':
        meta['elements'] = {
            'verbose_name': _('Elements'),
            'help_text': _('The questions and question sets for this question set.')
        }

    return meta


def get_languages() -> list[tuple]:
    languages = []
    for i in range(5):
        try:
            language = (settings.LANGUAGES[i][0], settings.LANGUAGES[i][1], f"lang{i + 1}")
            languages.append(language)
        except IndexError:
            pass
    return languages


def get_language_fields(field_name):
    return [
        field_name + '_' + lang_field for lang_code,
        lang_string, lang_field in get_languages()
        ]


def get_language_warning(obj, field):
    for lang_code, lang_string, lang_field in get_languages():
        if not getattr(obj, f'{field}_{lang_field}'):
            return True
    return False


def render_to_format(request, export_format, title, template_src, context):
    if export_format not in dict(settings.EXPORT_FORMATS):
        return HttpResponseBadRequest(_('This format is not supported.'))

    # render the template to a html string
    template = get_template(template_src)
    html = template.render(context)
    metadata, html = parse_metadata(html)

    # remove empty lines
    html = os.linesep.join([line for line in html.splitlines() if line.strip()])

    if export_format == 'html':
        # create the response object
        response = HttpResponse(html)
        response['Content-Disposition'] = f'filename="{title}.{export_format}"'

    else:
        pandoc_content = get_pandoc_content(html, metadata, export_format, context)
        pandoc_content_disposition = get_pandoc_content_disposition(export_format, title)

        response = HttpResponse(pandoc_content, content_type=f'application/{export_format}')
        response['Content-Disposition'] = pandoc_content_disposition.encode('utf-8')

    return response


def render_to_csv(title, rows, delimiter=','):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{title}.csv"'

    writer = csv.writer(response, delimiter=delimiter)
    for row in rows:
        writer.writerow(
            ['' if x is None else str(x) for x in row]
        )
    return response


def render_to_json(title, data, delimiter=','):
    response = HttpResponse(json.dumps(data, indent=2), content_type='text/json')
    response['Content-Disposition'] = f'attachment; filename="{title}.json"'
    return response


def return_file_response(file_path, content_type):
    file_abspath = Path(settings.MEDIA_ROOT) / file_path
    if file_abspath.exists():
        with file_abspath.open('rb') as fp:
            response = HttpResponse(fp.read(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename=' + file_abspath.name
            return response
    else:
        raise Http404


def sanitize_url(s):
    # is used in the rdmo-app
    try:
        m = re.search('[a-z0-9-_]', s)
    except TypeError:
        s = ''
    else:
        if bool(m) is False:
            s = ''
        else:
            s = re.sub(r'/+', '/', s)
    return s


def import_class(string):
    module_name, class_name = string.rsplit('.', 1)
    return getattr(importlib.import_module(module_name), class_name)


def copy_model(instance, **kwargs):
    # get values from instance which are not id, ForeignKeys or M2M relations
    data = {}
    for field in instance._meta.get_fields():
        if not (field.name == 'id' or field.is_relation):
            data[field.name] = getattr(instance, field.name)

    # update with the kwargs provided to this function
    data.update(kwargs)

    # create and save new instance
    instance_copy = instance._meta.model(**data)
    instance_copy.save()

    return instance_copy


def human2bytes(string):
    if not string or string == '0':
        return 0

    m = re.match(r'([0-9.]+)\s*([A-Za-z]+)', string)
    number, unit = float(m.group(1)), m.group(2).strip().lower()

    conversion = HUMAN2BYTES_MAPPER[unit]
    number = number*conversion['base']**(conversion['power'])
    return number


def is_truthy(value):
    return value is not None and (value is True or value.lower() in ['1', 't', 'true'])


def markdown2html(markdown_string):
    # adoption of the normal markdown function
    html = markdown(force_str(markdown_string)).strip()

    # strip the outer paragraph
    html = re.sub(r'^<p>(.*?)</p>$',r'\1', html)

    # convert `[<string>]{<title>}` to <span title="<title>"><string></span> to allow for underlined tooltips
    html = re.sub(
        r'\[(.*?)\]\{(.*?)\}',
        r'<span data-toggle="tooltip" data-placement="bottom" data-html="true" title="\2">\1</span>',
        html
    )

    # convert everything after `{more}` to <span class="more"><string></span> to be shown/hidden on user input
    show_string = _('show more')
    hide_string = _('show less')
    html = re.sub(
        r'(\{more\})(.*?)</p>$',
        f'<span class="show-more" onclick="showMore(this)">... ({show_string})</span>'
        r'<span class="more">\2</span>'
        f'<span class="show-less" onclick="showLess(this)"> ({hide_string})</span></p>',
        html
    )

    # textblocks (e.g. for help texts) can be injected into free text fields as small templates via Markdown
    html = inject_textblocks(html)

    return html


def inject_textblocks(html):
    # loop over all strings between curly brackets, e.g. {{ test }}
    for template_code in re.findall(r'{{(.*?)}}', html):
        template_name = settings.MARKDOWN_TEMPLATES.get(template_code.strip())
        if template_name:
            html = re.sub('{{' + template_code + '}}', render_to_string(template_name), html)
    return html


def parse_metadata(html):
    metadata = None
    pattern = re.compile(
        '(<metadata>)(.*)(</metadata>)', re.MULTILINE | re.DOTALL
    )
    m = re.search(pattern, html)
    if bool(m) is True:
        try:
            metadata = json.loads(m.group(2))
        except json.JSONDecodeError:
            pass
        else:
            html = html.replace(m.group(0), '')
    return metadata, html


def remove_double_newlines(string):
    return re.sub(r'[\n]{2,}', '\n\n', string)


def remove_html_special_characters(string):
    return re.sub(r'[<>&"\']', '', string)


def parse_date_from_string(date: str) -> datetime.date:
    if not isinstance(date, str):
        raise TypeError("date must be provided as string")

    try:
        # First, try standard ISO format (YYYY-MM-DD)
        parsed_date = parse_date(date)
    except ValueError as exc:
        raise exc from exc

    # If ISO parsing fails, try localized DATE_INPUT_FORMATS formats
    if parsed_date is None:
        for fmt in get_format('DATE_INPUT_FORMATS'):
            try:
                parsed_date = datetime.strptime(date, fmt).date()
                break  # Stop if parsing succeeds
            except ValueError:
                continue  # Try the next format

    # If still not parsed, raise an error
    if not parsed_date:
        raise ValueError(
            f"Invalid date format for: {date}. Valid formats {get_format('DATE_INPUT_FORMATS')}"
        )
    return parsed_date

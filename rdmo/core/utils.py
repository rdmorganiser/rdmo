import csv
import importlib
import logging
import os
import re
from tempfile import mkstemp
from urllib.parse import urlparse

import pypandoc
from django.apps import apps
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

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
    r = settings.DEFAULT_URI_PREFIX
    if bool(obj.uri_prefix) is True:
        r = obj.uri_prefix.rstrip('/')
    return r


def get_model_field_meta(model):
    meta = {}

    for field in model._meta.get_fields():
        meta[field.name] = {}
        if hasattr(field, 'verbose_name'):
            meta[field.name]['verbose_name'] = field.verbose_name
        if hasattr(field, 'help_text'):
            meta[field.name]['help_text'] = field.help_text

    return meta


def get_languages():
    languages = []
    for i in range(5):
        try:
            language = settings.LANGUAGES[i][0], settings.LANGUAGES[i][1], 'lang%i' % (i + 1)
            languages.append(language)
        except IndexError:
            pass
    return languages


def get_language_fields(field_name):
    return [field_name + '_' + lang_field for lang_code, lang_string, lang_field in get_languages()]


def get_language_warning(obj, field):
    for lang_code, lang_string, lang_field in get_languages():
        if not getattr(obj, '%s_%s' % (field, lang_field)):
            return True
    return False


def set_export_reference_document(format):
    refdoc_default = apps.get_app_config('rdmo').path + '/share/reference.' + format
    refdoc = refdoc_default

    if format == 'odt':
        try:
            settings.EXPORT_REFERENCE_ODT
        except AttributeError:
            pass
        else:
            refdoc = settings.EXPORT_REFERENCE_ODT
    elif format == 'docx':
        try:
            settings.EXPORT_REFERENCE_DOCX
        except AttributeError:
            pass
        else:
            refdoc = settings.EXPORT_REFERENCE_DOCX

    if os.path.isfile(refdoc) is False and os.path.isfile(refdoc_default) is True:
        refdoc = refdoc_default

    if os.path.isfile(refdoc) is False and os.path.isfile(refdoc_default) is False:
        refdoc = None

    return refdoc


def render_to_format(request, format, title, template_src, context):
    if format in dict(settings.EXPORT_FORMATS):

        # render the template to a html string
        template = get_template(template_src)
        html = template.render(context)

        # remove empty lines
        html = os.linesep.join([line for line in html.splitlines() if line.strip()])

        if format == 'html':

            # create the response object
            response = HttpResponse(html)

        else:
            if format == 'pdf':
                # check pandoc version (the pdf arg changed to version 2)
                if pypandoc.get_pandoc_version().split('.')[0] == '1':
                    args = ['-V', 'geometry:margin=1in', '--latex-engine=xelatex']
                else:
                    args = ['-V', 'geometry:margin=1in', '--pdf-engine=xelatex']

                content_disposition = 'filename="%s.%s"' % (title, format)
            else:
                args = []
                content_disposition = 'attachment; filename="%s.%s"' % (title, format)

            # use reference document for certain file formats
            refdoc = set_export_reference_document(format)
            if refdoc is not None and (format == 'docx' or format == 'odt'):
                if pypandoc.get_pandoc_version().startswith("1"):
                    refdoc_param = '--reference-' + format + '=' + refdoc
                    args.extend([refdoc_param])
                else:
                    refdoc_param = '--reference-doc=' + refdoc
                    args.extend([refdoc_param])

            # create a temporary file
            (tmp_fd, tmp_filename) = mkstemp('.' + format)

            log.info("Export " + format + " document using args " + str(args))
            # convert the file using pandoc
            pypandoc.convert_text(html, format, format='html', outputfile=tmp_filename, extra_args=args)

            # read the temporary file
            file_handler = os.fdopen(tmp_fd, 'rb')
            file_content = file_handler.read()
            file_handler.close()

            # delete the temporary file
            os.remove(tmp_filename)

            # create the response object
            response = HttpResponse(file_content, content_type='application/%s' % format)
            response['Content-Disposition'] = content_disposition.encode('utf-8')

        return response
    else:
        return HttpResponseBadRequest(_('This format is not supported.'))


def render_to_csv(title, rows, delimiter=','):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % title

    writer = csv.writer(response, delimiter=delimiter)
    for row in rows:
        writer.writerow(
            ['' if x is None else str(x) for x in row]
        )
    return response


# def pretty_print(data):
#     if type(data) == str:
#         data = json.dumps(data)
#     print(json.dumps(data, sort_keys=True, indent=4))


# def save_json(filename, data):
#     with open(filename, 'w') as outfile:
#         json.dump(data, outfile)


def sanitize_url(s):
    try:
        m = re.search('[a-z0-9-_]', s)
    except TypeError:
        s = ''
    else:
        if bool(m) is False:
            s = ''
        else:
            s = re.sub('/+', '/', s)
    return s


def import_class(string):
    module_name, class_name = string.rsplit('.', 1)
    return getattr(importlib.import_module(module_name), class_name)

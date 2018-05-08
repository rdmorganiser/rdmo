import csv
import os
import logging
import pypandoc
import re

import defusedxml.ElementTree as ET

from tempfile import mkstemp

from django.conf import settings
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.six.moves.urllib.parse import urlparse
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


def get_ns_map(treenode):
    nsmap = {}
    treestring = ET.tostring(treenode, encoding='utf8', method='xml')
    match = re.search(r'(xmlns:)(.*?)(=")(.*?)(")', str(treestring))
    if bool(match) is True:
        nsmap = {match.group(2): match.group(4)}
    log.info("Nsmap construction result: " + str(nsmap))
    return nsmap


def get_ns_tag(tag, nsmap):
    tag_split = tag.split(':')
    return '{%s}%s' % (nsmap[tag_split[0]], tag_split[1])


def get_uri(treenode, nsmap, method='text'):
    uri = None
    try:
        uri = treenode.find(get_ns_tag('dc:uri', nsmap))
    except Exception as e:
        log.error('URI fetching error: ' + str(e))
    if method == 'text':
        uri = uri.text
    elif method == 'attrib':
        uri = uri.attrib
    return uri


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
                    args = ['-V', 'geometry:margin=1in', '--pdf-engine=pdflatex']

                content_disposition = 'filename="%s.%s"' % (title, format)
            else:
                args = []
                content_disposition = 'attachment; filename="%s.%s"' % (title, format)

            # create a temporary file
            (tmp_fd, tmp_filename) = mkstemp('.' + format)

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


def render_to_csv(request, title, rows):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % title

    writer = csv.writer(response)

    for row in rows:
        writer.writerow(tuple(row))

    return response

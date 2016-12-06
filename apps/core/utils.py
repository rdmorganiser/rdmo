import os
import csv
from tempfile import mkstemp

import pypandoc

from django.conf import settings
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.six.moves.urllib.parse import urlparse
from django.utils.translation import ugettext_lazy as _


def get_script_alias(request):
    return request.path[:-len(request.path_info)]


def get_referer(request, default=None):
    return request.META.get('HTTP_REFERER', default)


def get_referer_path_info(request, default=None):
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


def render_to_format(request, format, title, template_src, context):

    # for some weird reason we have to cast here explicitly
    format = str(format)
    title = str(title)

    if format in settings.EXPORT_FORMATS:

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
                args = ['-V', 'geometry:margin=1in']
                content_disposition = 'filename=%s.%s' % (title, format)
            else:
                args = []
                content_disposition = 'attachment; filename=%s.%s' % (title, format)

            print (content_disposition)

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
            response['Content-Disposition'] = content_disposition

        return response
    else:
        return HttpResponseBadRequest(_('This format is not supported.'))


def render_to_csv(request, title, rows):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % title

    writer = csv.writer(response)

    for row in rows:
        writer.writerow(tuple(row))

    return response

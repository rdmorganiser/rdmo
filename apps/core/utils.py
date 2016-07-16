import os
from tempfile import mkstemp

from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.utils.six.moves.urllib.parse import urlparse
from django.utils.translation import ugettext_lazy as _

import pypandoc

def get_script_alias(request):
    return request.path[:-len(request.path_info)]


def get_referer_path_info(request, default=None):
    referer = request.META.get('HTTP_REFERER', None)
    if not referer:
        return default

    script_alias = get_script_alias(request)
    return urlparse(referer).path[len(script_alias):]


def get_referer(request):
    referer = request.META.get('HTTP_REFERER', None)
    if referer:
        return urlparse(referer).path
    else:
        return reverse('home')


def get_next(request):
    next = request.POST.get('next')

    if next in [request.path, '', None]:
        return reverse('home')
    else:
        return next


def get_internal_link(text, name, *args, **kwargs):
    url = reverse(name, args=args, kwargs=kwargs)

    if text is None:
        text = url

    return "<a href=\"%s\">%s</a>" % (url, text)


def render_to_format(request, template_src, context_dict, title, format):

    if format in settings.EXPORT_FORMATS:
        # render the template to a html string
        template = get_template(template_src)
        context = Context(context_dict)
        html = template.render(context).encode(encoding="UTF-8")

        # create a temporary file
        (tmp_fd, tmp_filename) = mkstemp('.' + format)

        # convert the file using pandoc
        pypandoc.convert_text(html, format, format='html', outputfile=tmp_filename)

        # read the temporary file
        file_handler = os.fdopen(tmp_fd)
        file_content = file_handler.read()
        file_handler.close()

        # delete the temporary file
        os.remove(tmp_filename)

        # create the response object and return
        response = HttpResponse(file_content, content_type='application/%s' % format)
        response['Content-Disposition'] = 'attachment; filename="%s.%s"' % (title, format)
        return response
    else:
        return HttpResponseBadRequest(_('This format is not supported.'))

def render_to_pdf():
    pass
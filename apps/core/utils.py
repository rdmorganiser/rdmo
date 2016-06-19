try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from xhtml2pdf import pisa

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

from cgi import escape

from django.core.urlresolvers import reverse, resolve, Resolver404
from django.utils.six.moves.urllib.parse import urlparse



def get_script_alias(request):
    return request.path[:-len(request.path_info)]


def get_referer_path_info(request, default=None):
    referer = request.META.get('HTTP_REFERER', None)
    if not referer:
        return default

    script_alias = get_script_alias(request)
    return urlparse(referer).path[len(script_alias):]


def get_referer_url_name(request, default=None):
    referer = request.META.get('HTTP_REFERER', None)
    if not referer:
        return default

    referer_path = urlparse(referer).path

    try:
        return resolve(referer_path).url_name
    except Resolver404:
        return default


def get_internal_link(text, name, *args, **kwargs):
    url = reverse(name, args=args, kwargs=kwargs)

    if text is None:
        text = url

    return "<a href=\"%s\">%s</a>" % (url, text)


def render_to_pdf(template_src, context_dict):
    '''
    taken from http://stackoverflow.com/questions/1377446/render-html-to-pdf-in-django-site
    '''
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

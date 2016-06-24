from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

from django.core.urlresolvers import reverse, resolve, Resolver404
from django.utils.six.moves.urllib.parse import urlparse

from weasyprint import HTML, CSS


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


def render_to_pdf(request, template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context).encode(encoding="UTF-8")

    filename = context_dict['title'] + '.pdf'

    pdf_file = HTML(string=html, base_url=request.build_absolute_uri(), encoding="utf8").write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = filename

    return response

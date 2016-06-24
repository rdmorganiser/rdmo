from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.six.moves.urllib.parse import urlparse

from weasyprint import HTML


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


def render_to_pdf(request, template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context).encode(encoding="UTF-8")

    filename = context_dict['title'] + '.pdf'

    pdf_file = HTML(string=html, base_url=request.build_absolute_uri(), encoding="utf8").write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = filename

    return response

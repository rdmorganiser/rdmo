from django.core.urlresolvers import reverse, resolve
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
    referer_url_name = resolve(referer_path).url_name

    return referer_url_name


def get_internal_link(text, name, *args, **kwargs):
    url = reverse(name, args=args, kwargs=kwargs)

    if text is None:
        text = url

    return "<a href=\"%s\">%s</a>" % (url, text)

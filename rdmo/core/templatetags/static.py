from django import template
from django.conf import settings
from django.templatetags.static import static as django_static

from rdmo import __version__

register = template.Library()

@register.simple_tag
def static(path):
    """
    Custom static tag that appends ?v={version} to all urls created with `{% static ... %}`.
    This overwrites the original django.templatetags.static.static.
    """
    static_url = django_static(path)

    if settings.DEBUG:
        return static_url
    else:
        if '?' in static_url:
            return f'{static_url}&v={__version__}'
        else:
            return f'{static_url}?v={__version__}'

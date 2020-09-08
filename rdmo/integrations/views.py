from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from .utils import get_integration


def oauth_callback(request, integration_key):
    integration = get_integration(request, integration_key)
    try:
        return integration.callback()
    except AssertionError:
        return render(request, 'core/error.html', {
            'title': _('Integration Error'),
            'errors': [_('Something went wrong. Please contact support.')]
        }, status=500)

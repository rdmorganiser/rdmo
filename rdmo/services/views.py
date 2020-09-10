from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from .utils import get_provider


def oauth_callback(request, provider_key):
    provider = get_provider(provider_key)
    try:
        return provider.callback(request)
    except AssertionError:
        return render(request, 'core/error.html', {
            'title': _('Integration Error'),
            'errors': [_('Something went wrong. Please contact support.')]
        }, status=500)

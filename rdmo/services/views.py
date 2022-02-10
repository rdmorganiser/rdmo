from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from rdmo.core.plugins import get_plugin

PROVIDER_TYPES = [
    'PROJECT_ISSUE_PROVIDERS',
    'PROJECT_EXPORTS',
    'PROJECT_IMPORTS'
]


def oauth_callback(request, provider_key):
    for provider_type in PROVIDER_TYPES:
        provider = get_plugin(provider_type, provider_key)
        if provider and provider.get_from_session(request, 'state'):
            return provider.callback(request)

    return render(request, 'core/error.html', {
        'title': _('Integration Error'),
        'errors': [_('Something went wrong. Please contact support.')]
    }, status=500)

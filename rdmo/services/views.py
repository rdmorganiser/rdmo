from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from rdmo.core.plugins import get_plugin

PROVIDER_TYPES = [
    'PROJECT_ISSUE_PROVIDERS',
    'PROJECT_EXPORTS',
    'PROJECT_IMPORTS'
]


def oauth_callback(request, provider_key):
    found = False
    for provider_type in PROVIDER_TYPES:
        provider = get_plugin(provider_type, provider_key)
        if provider is None:
            continue

        found = True
        provider.request = request

        if hasattr(provider, 'client') and provider.client.is_pending():
            return provider.client.callback()

    if not found:
        return render(request, 'core/error.html', {
            'title': _('OAuth authorization not successful'),
            'errors': [_('The service could not be found.')]
        }, status=404)

    # e.g. if the callback is opened again after the authorization was completed
    return render(request, 'core/error.html', {
        'title': _('OAuth authorization not successful'),
        'errors': [_('No authorization was started for this service, or it was already completed.')]
    }, status=400)

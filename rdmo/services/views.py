from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from rdmo.config.models import Plugin

PROVIDER_TYPES = [
    'PROJECT_ISSUE_PROVIDERS',
    'PROJECT_EXPORTS',
    'PROJECT_IMPORTS'
]


def oauth_callback(request, provider_key):
    for plugin in (Plugin.objects.
            for_context(user=request.user, format=provider_key)
            .filter(plugin_type__in=PROVIDER_TYPES)
    ):
        provider = plugin.initialize_class()
        if provider and provider.get_from_session(request, 'state'):
            return provider.callback(request)

    return render(request, 'core/error.html', {
        'title': _('Integration Error'),
        'errors': [_('Something went wrong. Please contact support.')]
    }, status=500)

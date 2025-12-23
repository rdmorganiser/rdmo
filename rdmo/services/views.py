from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from rdmo.config.constants import PLUGIN_TYPES
from rdmo.config.models import Plugin

PROVIDER_TYPES = [
    PLUGIN_TYPES.PROJECT_ISSUE_PROVIDER,
    PLUGIN_TYPES.PROJECT_EXPORT,
    PLUGIN_TYPES.PROJECT_IMPORT,
]


def oauth_callback(request, provider_key):
    for plugin in (Plugin.objects.for_context(
            user=request.user,
            format=provider_key,
            plugin_types=PROVIDER_TYPES
        )
    ):
        provider = plugin.initialize_class()
        if provider and provider.get_from_session(request, 'state'):
            return provider.callback(request)

    return render(request, 'core/error.html', {
        'title': _('Integration Error'),
        'errors': [_('Something went wrong. Please contact support.')]
    }, status=500)

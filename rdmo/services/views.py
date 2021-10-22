from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from rdmo.core.plugins import get_plugin


def oauth_callback(request, provider_key):
    provider = get_plugin('PROJECT_ISSUE_PROVIDERS', provider_key) or \
               get_plugin('PROJECT_EXPORT_PROVIDERS', provider_key)

    try:
        return provider.callback(request)
    except AssertionError:
        return render(request, 'core/error.html', {
            'title': _('Integration Error'),
            'errors': [_('Something went wrong. Please contact support.')]
        }, status=500)

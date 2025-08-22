from __future__ import annotations

from django.conf import settings
from django.core.checks import Tags, Warning, register

W_MISSING_FIX = "rdmo.accounts.W001"
W_FIX_DISABLED = "rdmo.accounts.W002"



@register(Tags.compatibility)
def check_shibboleth_remoteuser(app_configs=None, **kwargs):
    """Warn when the installed shibboleth package lacks the URL-decoding fix
    or when the fix exists but isn't enabled.
    """
    if (
        "shibboleth" not in settings.INSTALLED_APPS
        and not getattr(settings, "SHIBBOLETH", False)
    ):
        return []

    try:
        from shibboleth import app_settings as shib_settings
    except ModuleNotFoundError:
        return []

    messages = []

    has_unquote_flag = hasattr(shib_settings, "UNQUOTE_ATTRIBUTES")
    if not has_unquote_flag:
        messages.append(
            Warning(
                "Installed 'django-shibboleth-remoteuser' lacks the URL-decoding "
                "feature for UTF-8 attributes (UNQUOTE_ATTRIBUTES). Umlauts and "
                "other non-ASCII characters may be stored incorrectly.",
                obj="SHIBBOLETH",
                hint=(
                    "Replace the upstream package with the RDMO fork, forcing a reinstall:\n"
                    "    pip install -U --force-reinstall --no-deps "
                    "\"django-shibboleth-remoteuser @ "
                    "git+https://github.com/rdmorganiser/django-shibboleth-remoteuser@main\"\n"
                    "Then set SHIBBOLETH_UNQUOTE_ATTRIBUTES = True in your settings."
                ),
                id=W_MISSING_FIX,
            )
        )
        return messages

    if not getattr(settings, "SHIBBOLETH_UNQUOTE_ATTRIBUTES", False):
        messages.append(
            Warning(
                "SHIBBOLETH_UNQUOTE_ATTRIBUTES is not enabled. "
                "URL-encoded Shibboleth attributes will not be percent-decoded, "
                "which can break Umlauts and other UTF-8 characters.",
                obj="SHIBBOLETH_UNQUOTE_ATTRIBUTES",
                hint="Set SHIBBOLETH_UNQUOTE_ATTRIBUTES = True in your Django settings.",
                id=W_FIX_DISABLED,
            )
        )

    return messages

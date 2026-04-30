from django.conf import settings

from rdmo.config.constants import PLUGIN_TYPES


def get_plugins_from_legacy_settings() -> list[dict]:
    """Read 3-tuples (key, label, python-path) from legacy settings."""
    plugin_definitions: list[dict] = []
    for legacy_setting, plugin_type in (
        ("PROJECT_IMPORTS", PLUGIN_TYPES.PROJECT_IMPORT),
        ("PROJECT_EXPORTS", PLUGIN_TYPES.PROJECT_EXPORT),
        ("PROJECT_SNAPSHOT_EXPORTS", PLUGIN_TYPES.PROJECT_SNAPSHOT_EXPORT),
        ("PROJECT_ISSUE_PROVIDERS", PLUGIN_TYPES.PROJECT_ISSUE_PROVIDER),
        ("OPTIONSET_PROVIDERS", PLUGIN_TYPES.OPTIONSET_PROVIDER),
    ):

        legacy_plugins = getattr(settings, legacy_setting, [])
        if not legacy_plugins:
            continue

        for (key, label, dotted) in legacy_plugins:

            plugin_definitions.append({
                "uri_prefix": settings.DEFAULT_URI_PREFIX,
                "uri_path": f"{legacy_setting.lower()}/{key}",
                "title": label,
                "python_path": dotted,
                "plugin_type": plugin_type,
                "url_name": key,
            })

    return plugin_definitions

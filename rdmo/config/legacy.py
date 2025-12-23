from django.conf import settings

from rdmo.config.constants import PLUGIN_TYPES

PLUGIN_TYPE_TO_SETTING_KEY = {
    PLUGIN_TYPES.PROJECT_IMPORT: "PROJECT_IMPORTS",
    PLUGIN_TYPES.PROJECT_EXPORT: "PROJECT_EXPORTS",
    PLUGIN_TYPES.PROJECT_SNAPSHOT_EXPORT: "PROJECT_SNAPSHOT_EXPORTS",
    PLUGIN_TYPES.PROJECT_ISSUE_PROVIDER: "PROJECT_ISSUE_PROVIDERS",
    PLUGIN_TYPES.OPTIONSET_PROVIDER: "OPTIONSET_PROVIDERS",
}

def get_plugins_from_legacy_settings(select_plugin_type=None) -> list[dict]:
    """Read 3-tuples (key, label, python-path) from legacy settings."""
    plugin_definitions: list[dict] = []
    for plugin_type, legacy_setting in PLUGIN_TYPE_TO_SETTING_KEY.items():
        if not hasattr(settings, legacy_setting):
            continue
        if select_plugin_type is not None and select_plugin_type != plugin_type:
            continue

        legacy_plugins = getattr(settings, legacy_setting, None)
        if not legacy_plugins:
            continue

        for entry in legacy_plugins:
            try:
                key, label, dotted = entry
            except Exception as exc:
                raise ValueError(
                    f"{legacy_setting} must be a sequence of 3-tuples "
                    f"(key, label, python-path); got {entry!r}"
                ) from exc

            plugin_definitions.append({
                "uri_prefix": settings.DEFAULT_URI_PREFIX,
                "uri_path": f"{legacy_setting.lower()}/{key}",
                "title": label,
                "python_path": dotted,
                "plugin_type": plugin_type,
                "url_name": key,
            })

    return plugin_definitions

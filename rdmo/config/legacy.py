from __future__ import annotations

from django.conf import settings

from rdmo.config.constants import PluginType
from rdmo.config.helpers import DeclaredPlugin
from rdmo.config.utils import get_default_uri_prefix_for_python_path

LEGACY_PLUGIN_SETTINGS = [
        "PROJECT_EXPORTS",
        "PROJECT_SNAPSHOT_EXPORTS",
        "PROJECT_IMPORTS",
        "PROJECT_IMPORTS_LIST",
        "PROJECT_ISSUE_PROVIDERS",
        "OPTIONSET_PROVIDERS",
    ]

PLUGIN_TYPE_TO_SETTING_KEY = {
    PluginType.PROJECT_IMPORT: "PROJECT_IMPORTS",
    PluginType.PROJECT_EXPORT: "PROJECT_EXPORTS",
    PluginType.PROJECT_SNAPSHOT_EXPORT: "PROJECT_SNAPSHOT_EXPORTS",
    PluginType.PROJECT_ISSUE_PROVIDER: "PROJECT_ISSUE_PROVIDERS",
    PluginType.OPTIONSET_PROVIDER: "OPTIONSET_PROVIDERS",
}

def get_plugins_from_legacy_settings(select_plugin_type=None) -> list[DeclaredPlugin]:
    """Read 3-tuples (key, label, python-path) from legacy settings."""
    declared: list[DeclaredPlugin] = []
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

            declared.append(
                DeclaredPlugin(
                    uri_prefix=get_default_uri_prefix_for_python_path(dotted),
                    uri_path=f"{legacy_setting.lower()}/{key}",
                    title=label,
                    python_path=dotted,
                    plugin_type=plugin_type,
                    url_name=key,
                    source=legacy_setting
                )
            )
    return declared  # normalize within legacy list

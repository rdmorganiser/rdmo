from __future__ import annotations

from django.conf import settings

from rdmo.config.helpers import DeclaredPlugin
from rdmo.config.utils import get_default_uri_prefix_for_python_path

from .plugin_type_constants import PluginType

PLUGIN_TYPE_LEGACY_SETTING_MAP = {
    PluginType.PROJECT_IMPORT.value: ("PROJECT_IMPORTS", "PROJECT_IMPORTS_LIST"),
    PluginType.PROJECT_EXPORT.value: ("PROJECT_EXPORTS", None),
    "project_snapshot_export": ("PROJECT_SNAPSHOT_EXPORTS", None),
    PluginType.PROJECT_ISSUE_PROVIDER.value: ("PROJECT_ISSUE_PROVIDERS", None),
    PluginType.OPTIONSET_PROVIDER.value: ("OPTIONSET_PROVIDERS", None),
}

def get_plugins_from_legacy_settings(select_plugin_type=None) -> list[DeclaredPlugin]:
    """Read 3-tuples (key, label, python-path) from legacy settings."""
    declared: list[DeclaredPlugin] = []
    for plugin_type, (setting_name, _) in PLUGIN_TYPE_LEGACY_SETTING_MAP.items():
        if not hasattr(settings, setting_name):
            continue
        if select_plugin_type is not None and select_plugin_type != plugin_type:
            continue

        legacy_plugins = getattr(settings, setting_name, None)
        if not legacy_plugins:
            continue

        for entry in legacy_plugins:
            try:
                key, label, dotted = entry
            except Exception as exc:
                raise ValueError(
                    f"{setting_name} must be a sequence of 3-tuples "
                    f"(key, label, python-path); got {entry!r}"
                ) from exc

            declared.append(
                DeclaredPlugin(
                    uri_prefix=get_default_uri_prefix_for_python_path(dotted),
                    uri_path=f"{setting_name.lower()}/{key}",
                    title=label,
                    python_path=dotted,
                    plugin_type=plugin_type,
                    url_name=key,
                    source=setting_name
                )
            )
    return declared  # normalize within legacy list

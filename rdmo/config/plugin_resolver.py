from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from django.conf import settings
from django.utils.module_loading import import_string

from rdmo.config.models import Plugin
from rdmo.config.plugins import detect_plugin_type
from rdmo.config.utils import get_default_uri_prefix_for_python_path

PLUGIN_TYPE_LEGACY_SETTING_MAP = {
    "project_import": ("PROJECT_IMPORTS", "PROJECT_IMPORTS_LIST"),
    "project_export": ("PROJECT_EXPORTS", None),
    "project_snapshot_export": ("PROJECT_SNAPSHOT_EXPORTS", None),
    "project_issue_provider": ("PROJECT_ISSUE_PROVIDERS", None),
    "optionset_provider": ("OPTIONSET_PROVIDERS", None),
}

PLUGINS_URL_NAMES = {
    "rdmo.projects.exports.RDMOXMLExport": "xml",
    "rdmo.projects.exports.CSVCommaExport": "csvcomma",
    "rdmo.projects.exports.CSVSemicolonExport": "csvsemicolon",
    "rdmo.projects.exports.JSONExport": "json",
    "rdmo.projects.imports.RDMOXMLImport": "xml",
}


@dataclass(frozen=True)
class DeclaredPlugin:
    uri_prefix: str
    uri_path: str  # is the key for legacy settings
    python_path: str
    title: str = field(repr=False)
    plugin_type: str
    plugin_settings: dict[str, Any] | None = field(default_factory=dict, repr=False)
    url_name: str | None = ""  # also the key for legacy settings
    source: str | None = None  # from legacy setting or db

    def get_plugin_instance(self):
        try:
            from django.utils.module_loading import import_string
            return import_string(self.python_path)(self.uri_path, self.title, self.python_path)
        except Exception:
            return None


def list_and_filter_plugins(plugin_type: str | None = None, project=None, user=None) -> list[DeclaredPlugin]:
    legacy = get_plugins_from_legacy_settings(select_plugin_type=plugin_type)
    if not settings.PLUGINS:  # plugins still need to be enabled via settings
        return legacy

    current = get_plugins_from_db(project=project, plugin_type=plugin_type, user=user)
    merged = []
    for python_path in settings.PLUGINS:
        in_legacy = [i for i in legacy if i.python_path == python_path]
        in_current = [i for i in current if i.python_path == python_path]
        if in_current:
            merged += in_current
        elif in_legacy:
            merged += in_legacy

    return merged


# ----- Internals: legacy settings translation -----------------------

def get_plugins_from_legacy_settings(select_plugin_type=None) -> list[DeclaredPlugin]:
    """Read 3-tuples (key, label, python-path) from legacy settings."""
    declared: list[DeclaredPlugin] = []
    for plugin_type, (setting_name, allowlist_name) in PLUGIN_TYPE_LEGACY_SETTING_MAP.items():
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


def get_plugins_from_current_setting() -> list[DeclaredPlugin]:
    """
    Read python paths from settings.PLUGINS and infer key/title.
    Try to import the class to obtain nicer metadata when available.
    """
    if not hasattr(settings, "PLUGINS"):
        return []

    declared: list[DeclaredPlugin] = []
    for python_path in settings.PLUGINS:

        url_name = PLUGINS_URL_NAMES.get(python_path, "")
        try:
            cls = import_string(python_path)
        except Exception:
            cls = None

        if cls is not None:
            uri_path = getattr(cls, "key", None) or url_name or cls.__name__.lower()
            title = getattr(cls, "label", None) or getattr(cls, "title", None) or cls.__name__
            plugin_type = detect_plugin_type(cls)
        else:
            uri_path = url_name or python_path.replace(".", "_")
            title = python_path.rsplit(".", 1)[-1]
            plugin_type = "unknown_plugin_type"

        declared.append(
            DeclaredPlugin(
                title=title,
                python_path=python_path,
                uri_prefix=get_default_uri_prefix_for_python_path(python_path),
                uri_path=uri_path,
                plugin_type=plugin_type,
                url_name=url_name,
                source="PLUGINS"
            )
        )
    return declared


def get_plugins_from_db(project=None, plugin_type: str | None=None, user=None) -> list[DeclaredPlugin]:
    """
    Pull available plugins for the given project, then keep only rows whose class
    inherits the correct base (e.g. Import/Export/Provider).
    """
    if not settings.PLUGINS:
        return []

    qs = Plugin.objects.all()
    if project is not None:
        qs = Plugin.objects.filter_for_project(project)

    if user is not None:
        qs = qs.filter_current_available(user)
    else:
        qs = qs.filter(available=True).filter_current_site()

    qs = qs.order_by("order", "uri")

    results: list[DeclaredPlugin] = []
    for instance in qs:

        try:
            _ = instance.get_class()  # raises if import_string fails;
        except Exception:
            continue

        if instance.python_path not in settings.PLUGINS:
            continue

        if instance.plugin_type != plugin_type:
            continue

        results.append(DeclaredPlugin(
            uri_prefix=instance.uri_prefix,
            uri_path=instance.uri_path,
            python_path=instance.python_path,
            title=instance.title or instance.uri_path,
            plugin_type=instance.plugin_type,
            url_name=instance.url_name,
            source=f"Plugin(id={instance.id})",
        ))
    return results

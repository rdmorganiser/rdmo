from __future__ import annotations

from django.conf import settings
from django.utils.module_loading import import_string

from rdmo.config.helpers import DeclaredPlugin
from rdmo.config.legacy import get_plugins_from_legacy_settings
from rdmo.config.plugin_types import detect_plugin_type
from rdmo.config.plugins import get_plugins_from_db
from rdmo.config.utils import get_default_uri_prefix_for_python_path

PLUGINS_URL_NAMES = {
    "rdmo.projects.exports.RDMOXMLExport": "xml",
    "rdmo.projects.exports.CSVCommaExport": "csvcomma",
    "rdmo.projects.exports.CSVSemicolonExport": "csvsemicolon",
    "rdmo.projects.exports.JSONExport": "json",
    "rdmo.projects.imports.RDMOXMLImport": "xml",
}


def list_and_filter_plugins(plugin_type: str | None = None, project=None, user=None) -> list[DeclaredPlugin]:
    if not settings.PLUGINS:  # plugins still need to be enabled via settings
        legacy = get_plugins_from_legacy_settings(select_plugin_type=plugin_type)
        return legacy

    current = get_plugins_from_db(project=project, plugin_type=plugin_type, user=user)
    filtered = [i for i in current if i.python_path in settings.PLUGINS]
    return filtered


def get_plugins_from_current_setting() -> list[DeclaredPlugin]:
    """
    Read python paths from settings.PLUGINS and infer key/title.
    Try to import the class to obtain nicer metadata when available.
    """
    if not hasattr(settings, "PLUGINS"):
        return []

    declared: list[DeclaredPlugin] = []
    for python_path in settings.PLUGINS:
        if not python_path:
            continue

        url_name = PLUGINS_URL_NAMES.get(python_path, "")
        try:
            cls = import_string(python_path)
        except Exception:
            cls = None

        plugin_type = detect_plugin_type(python_path)

        if cls is not None:
            uri_path = getattr(cls, "key", None) or url_name or cls.__name__.lower()
            title = getattr(cls, "label", None) or getattr(cls, "title", None) or cls.__name__
        else:
            title = python_path.split(".")[-1]
            if url_name:
                uri_path = url_name
            else:
                _python_path_slug = python_path.replace(".", "-")
                uri_path = _python_path_slug

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

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from rdmo.config.constants import PLUGIN_TYPES

PLUGINS_URL_NAMES = {
    "rdmo.projects.exports.RDMOXMLExport": "xml",
    "rdmo.projects.exports.CSVCommaExport": "csvcomma",
    "rdmo.projects.exports.CSVSemicolonExport": "csvsemicolon",
    "rdmo.projects.exports.JSONExport": "json",
    "rdmo.projects.imports.RDMOXMLImport": "xml",
}



def get_plugin_type_mapping():
    # imports at run-time only
    from rdmo.options.providers import Provider
    from rdmo.projects.exports import Export
    from rdmo.projects.imports import Import
    from rdmo.projects.providers import IssueProvider

    plugin_type_mapping = {
        PLUGIN_TYPES.PROJECT_EXPORT: Export,
        PLUGIN_TYPES.PROJECT_IMPORT: Import,
        PLUGIN_TYPES.PROJECT_ISSUE_PROVIDER: IssueProvider,
        PLUGIN_TYPES.OPTIONSET_PROVIDER: Provider,
    }
    return plugin_type_mapping


def detect_plugin_type(python_path) -> PLUGIN_TYPES | str:
    from rdmo.config.plugins import BasePlugin

    try:
        plugin_class = import_string(python_path)
    except ImportError as e:
        raise ValidationError(f"Could not import plugin from {python_path}: {e}") from e

    if hasattr(plugin_class, "plugin_type"):
        if plugin_class.plugin_type:
            try:
                return PLUGIN_TYPES(plugin_class.plugin_type)
            except ValueError:
                return plugin_class.plugin_type
        else:
            return "has_plugin_type_but_empty"

    if not issubclass(plugin_class, BasePlugin):
        return "not_an_rdmo_plugin"

    for plugin_type, internal_plugin_class in get_plugin_type_mapping().items():
        if issubclass(plugin_class, internal_plugin_class):
            return plugin_type

    return "unknown_plugin_type"


def get_plugins_from_settings() -> list[dict]:
    """
    Read python paths from settings.PLUGINS and infer key/title.
    Try to import the class to obtain nicer metadata when available.
    """
    if not settings.PLUGINS:
        return []

    plugin_definitions = []
    errors = []
    for python_path in settings.PLUGINS:
        url_name = PLUGINS_URL_NAMES.get(python_path, "")
        try:
            plugin_class = import_string(python_path)
        except ImportError as e:
            errors.append(_("Could not import plugin from %(path)s: %(err)s") % {
                "path": python_path,
                "err": str(e),
            })
            continue

        try:
            plugin_type = detect_plugin_type(python_path)
        except ValidationError as e:
            errors.extend(e.messages)
            continue

        if plugin_class is not None:
            uri_path = getattr(plugin_class, "key", None) or url_name or plugin_class.__name__.lower()
            title = (getattr(plugin_class, "label", None) or getattr(plugin_class, "title", None)
                     or plugin_class.__name__)
            uri_prefix = (
                    getattr(plugin_class, "uri_prefix", None)
                    or getattr(plugin_class, "default_uri_prefix", None)
                    or settings.DEFAULT_URI_PREFIX
            )
        else:
            title = python_path.split(".")[-1]
            if url_name:
                uri_path = url_name
            else:
                uri_path = python_path.replace(".", "-")
            uri_prefix = settings.DEFAULT_URI_PREFIX

        plugin_definitions.append({
            "title": title,
            "python_path": python_path,
            "uri_prefix": uri_prefix,
            "uri_path": uri_path,
            "plugin_type": plugin_type,
            "url_name": url_name,
        })

    if errors:
        raise ValidationError(errors)

    return plugin_definitions

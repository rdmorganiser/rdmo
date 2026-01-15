from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

PLUGINS_URL_NAMES = {
    "rdmo.projects.exports.RDMOXMLExport": "xml",
    "rdmo.projects.exports.CSVCommaExport": "csvcomma",
    "rdmo.projects.exports.CSVSemicolonExport": "csvsemicolon",
    "rdmo.projects.exports.JSONExport": "json",
    "rdmo.projects.imports.RDMOXMLImport": "xml",
}


def get_plugin_type_from_class(plugin_class) -> str:
    try:
        if plugin_class.plugin_type:
            return plugin_class.plugin_type
        else:
            raise ValueError("Plugin type defined but empty.") from None
    except AttributeError as e:
        raise ValueError("Plugin type missing.") from e


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
        try:
            plugin_class = import_string(python_path)
        except ImportError as e:
            errors.append(_("Could not import plugin from %(path)s: %(err)s") % {
                "path": python_path,
                "err": str(e),
            })
            continue

        try:
            plugin_type = get_plugin_type_from_class(plugin_class)
        except ValueError as e:
            errors.append(_("Could not get plugin type from %(path)s: %(err)s") % {
                "path": python_path,
                "err": str(e),
            })
            continue

        url_name = (
            PLUGINS_URL_NAMES.get(python_path)
            or getattr(plugin_class, "url_name", None)
            or getattr(plugin_class, "key", None)
        )
        uri_path = (
            getattr(plugin_class, "uri_path", None)
            or getattr(plugin_class, "key", None)
            or url_name or plugin_class.__name__.lower()
        )
        uri_prefix = (
            getattr(plugin_class, "uri_prefix", None)
            or getattr(plugin_class, "default_uri_prefix", None)
            or settings.DEFAULT_URI_PREFIX
        )
        title = (
            getattr(plugin_class, "title", "")
            or getattr(plugin_class, "label", "")
            or plugin_class.__name__
        )

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

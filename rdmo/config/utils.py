from django.conf import settings
from django.utils.module_loading import import_string

PLUGINS_URL_NAMES = {
    "rdmo.projects.exports.RDMOXMLExport": "xml",
    "rdmo.projects.exports.CSVCommaExport": "csvcomma",
    "rdmo.projects.exports.CSVSemicolonExport": "csvsemicolon",
    "rdmo.projects.exports.JSONExport": "json",
    "rdmo.projects.imports.RDMOXMLImport": "xml",
}


def get_plugins_from_settings() -> list[dict]:
    """
    Read python paths from settings.PLUGINS and infer url_name/title.
    Try to import the class to obtain nicer metadata when available.
    """
    if not settings.PLUGINS:
        return []

    plugin_definitions = []
    for python_path in settings.PLUGINS:
        plugin_class = import_string(python_path)
        plugin_type = plugin_class.plugin_type

        url_name = (
            PLUGINS_URL_NAMES.get(python_path)
            or getattr(plugin_class, "url_name", None)
        )
        uri_path = (
            getattr(plugin_class, "uri_path", None)
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

    return plugin_definitions


def get_plugin_python_paths(raise_exception=False):
    plugin_paths = []
    for python_path in settings.PLUGINS:
        try:
            import_string(python_path)
        except (ImportError, ValueError) as e:
            if raise_exception:
                raise e from e
        else:
            plugin_paths.append(python_path)
    return plugin_paths

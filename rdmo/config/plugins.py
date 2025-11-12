from django.utils.module_loading import import_string

from rdmo.core.plugins import Plugin as PluginBase

PLUGIN_TYPES = {
    "project_export": "rdmo.projects.exports.Export",
    "project_import": "rdmo.projects.imports.Import",
    "project_issue_provider": "rdmo.projects.providers.IssueProvider",
    "optionset_provider": "rdmo.options.providers.Provider",
}


def detect_plugin_type(cls_or_instance) -> str:
    is_instance = not isinstance(cls_or_instance, type)
    cls = cls_or_instance.__class__ if is_instance else cls_or_instance

    if not issubclass(cls, PluginBase):
        return "not_an_rdmo_plugin"

    for plugin_type, python_path  in PLUGIN_TYPES.items():
        plugin_base_class = import_string(python_path)
        if issubclass(cls, plugin_base_class):
            return plugin_type

    return "unknown_plugin_type"

from django.utils.module_loading import import_string

from rdmo.core.plugins import Plugin as PluginBase

PLUGIN_BASES = (
    ("project_export", "rdmo.projects.exports.Export"),
    ("project_import", "rdmo.projects.imports.Import"),
    ("project_issue_provider", "rdmo.projects.providers.IssueProvider"),
    ("optionset_provider", "rdmo.options.providers.Provider"),
)


PLUGIN_TYPES = {key: import_string(dotted) for key, dotted in PLUGIN_BASES}


def detect_plugin_type(cls_or_instance) -> str:
    is_instance = not isinstance(cls_or_instance, type)
    cls = cls_or_instance.__class__ if is_instance else cls_or_instance

    if not issubclass(cls, PluginBase):
        return "not_an_rdmo_plugin"

    for plugin_type, plugin_base_cls in PLUGIN_TYPES.items():
        if issubclass(cls, plugin_base_cls):
            return plugin_type

    return "unknown_plugin_type"

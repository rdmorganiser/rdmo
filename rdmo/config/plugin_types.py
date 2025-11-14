from __future__ import annotations

from django.utils.module_loading import import_string

from rdmo.core.plugins import Plugin as LegacyPluginBase


def get_plugin_type_mapping():
    from rdmo.options.providers import Provider
    from rdmo.projects.exports import Export
    from rdmo.projects.imports import Import
    from rdmo.projects.providers import IssueProvider

    PLUGIN_TYPE_MAPPING = {
        "project_export": Export,
        "project_import": Import,
        "project_issue_provider": IssueProvider,
        "optionset_provider": Provider,
    }
    return PLUGIN_TYPE_MAPPING


def detect_plugin_type(python_path) -> str:
    try:
        cls = import_string(python_path)
    except ImportError:
        return "import_error"
    except ValueError:
        return "import_value_error"

    if hasattr(cls, "plugin_type"):
        if cls.plugin_type:
            return cls.plugin_type
        else:
            return "plugin_type_set_but_empty"

    if not issubclass(cls, LegacyPluginBase):
        return "not_an_rdmo_plugin"

    for plugin_type, plugin_class  in get_plugin_type_mapping().items():
        if issubclass(cls, plugin_class):
            return plugin_type

    return "unknown_plugin_type"

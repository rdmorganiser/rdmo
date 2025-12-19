from __future__ import annotations

from django.utils.module_loading import import_string

from .plugin_type_constants import PluginType


def get_plugin_type_mapping():
    # imports at run-time only
    from rdmo.options.providers import Provider
    from rdmo.projects.exports import Export
    from rdmo.projects.imports import Import
    from rdmo.projects.providers import IssueProvider

    plugin_type_mapping = {
        PluginType.PROJECT_EXPORT: Export,
        PluginType.PROJECT_IMPORT: Import,
        PluginType.PROJECT_ISSUE_PROVIDER: IssueProvider,
        PluginType.OPTIONSET_PROVIDER: Provider,
    }
    return plugin_type_mapping


def detect_plugin_type(python_path) -> PluginType | str:
    try:
        cls = import_string(python_path)
    except ImportError:
        return "import_error"
    except ValueError:
        return "import_value_error"

    if hasattr(cls, "plugin_type"):
        if cls.plugin_type:
            try:
                return PluginType(cls.plugin_type)
            except ValueError:
                return cls.plugin_type
        else:
            return "has_plugin_type_but_empty"

    from rdmo.config.plugins import PluginBase as LegacyPluginBase
    if not issubclass(cls, LegacyPluginBase):
        return "not_an_rdmo_plugin"

    for plugin_type, plugin_class in get_plugin_type_mapping().items():
        if issubclass(cls, plugin_class):
            return plugin_type

    if hasattr(cls, "get_options"):
        return PluginType.OPTIONSET_PROVIDER

    return "unknown_plugin_type"

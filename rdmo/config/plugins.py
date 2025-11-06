from rdmo.core.plugins import Plugin
from rdmo.options.providers import Provider as OptionsetProvider
from rdmo.projects.exports import Export
from rdmo.projects.imports import Import
from rdmo.projects.providers import IssueProvider

PLUGIN_BASES = {
    'OPTIONSET_PROVIDER': OptionsetProvider,
    'PROJECT_EXPORT': Export,
    'PROJECT_IMPORT': Import,
    'PROJECT_ISSUE_PROVIDER': IssueProvider,
}

def detect_plugin_type(plugin_class):
    if not issubclass(plugin_class, Plugin):
        return "not_an_rdmo_plugin"

    for type_name, base_cls in PLUGIN_BASES.items():
        if issubclass(plugin_class, base_cls):
            return type_name
    return 'rdmo_plugin_unknown_type'

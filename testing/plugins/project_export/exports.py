from rdmo.projects.exports import JSONExport


class SimpleExportPlugin(JSONExport):
    default_uri_prefix = "https://rdmorganiser.github.io/terms"
    settings_defaults = {
        'TIMEOUT': 10,
    }
    settings_namespace = 'SIMPLE_EXPORT_PLUGIN'

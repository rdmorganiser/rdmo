from rdmo.projects.exports import JSONExport


class SimpleExportPlugin(JSONExport):
    default_uri_prefix = "https://rdmorganiser.github.io/terms"

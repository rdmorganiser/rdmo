from django.db.models import TextChoices


class PLUGIN_TYPES(TextChoices):
    PROJECT_EXPORT = "project_export", "Project export"
    PROJECT_SNAPSHOT_EXPORT = "project_snapshot_export", "Project snapshot export"
    PROJECT_IMPORT = "project_import", "Project import"
    PROJECT_ISSUE_PROVIDER = "project_issue_provider", "Project issue provider"
    OPTIONSET_PROVIDER = "optionset_provider", "Optionset provider"


LEGACY_PLUGIN_SETTINGS = (
    'PROJECT_EXPORTS',
    'PROJECT_IMPORTS',
    'PROJECT_SNAPSHOT_EXPORTS',
    'PROJECT_ISSUE_PROVIDERS',
    'OPTIONSET_PROVIDERS',
)

PLUGIN_META_ATTRIBUTES = (
    'accept',
    'upload',
    'search',
    'refresh',
    'delimiter',
    'distribution_name',
    'distribution_version',
)

PLUGINS_URL_NAMES = {
    "rdmo.projects.exports.RDMOXMLExport": "xml",
    "rdmo.projects.exports.CSVCommaExport": "csvcomma",
    "rdmo.projects.exports.CSVSemicolonExport": "csvsemicolon",
    "rdmo.projects.exports.JSONExport": "json",
    "rdmo.projects.imports.RDMOXMLImport": "xml",
}

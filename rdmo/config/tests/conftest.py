import pytest

from django.utils.translation import gettext_lazy as _


@pytest.fixture
def enable_legacy_plugins(settings):

    delattr(settings, 'PLUGINS')
    # settings.INSTALLED_APPS has 'plugins' already
    # insert the relevant legacy plugin-tuples in settings,
    # e.g. PROJECT_EXPORTS, PROJECT_IMPORTS, OPTIONSET_PROVIDERS
    # to support the backwards compatible settings
    settings.PROJECT_EXPORTS = [
        ('xml', _('RDMO XML'), 'rdmo.projects.exports.RDMOXMLExport'),
        ('csvcomma', _('CSV (comma separated)'), 'rdmo.projects.exports.CSVCommaExport'),
        ('csvsemicolon', _('CSV (semicolon separated)'), 'rdmo.projects.exports.CSVSemicolonExport'),
        ('json', _('JSON'), 'rdmo.projects.exports.JSONExport'),
        ("simple_export", "Test Export", "plugins.project_export.exports.SimpleExportPlugin"),
    ]
    settings.PROJECT_IMPORTS = [
        ('xml', _('RDMO XML'), 'rdmo.projects.imports.RDMOXMLImport'),
        ('url', _('from URL'), 'rdmo.projects.imports.URLImport'),
    ]

    settings.PROJECT_SNAPSHOT_EXPORTS = [
        ("simple_snapshot_export", "Snapshot RDMO XML", "plugins.project_snapshot_export.exports.SimpleSnapshotExportPlugin"),  # noqa: E501
    ]

    settings.OPTIONSET_PROVIDERS = [
        ("simple_optionset_provider", "Simple OptionSet Provider", "plugins.optionset_providers.providers.SimpleProvider"),  # noqa: E501
    ]

    settings.PROJECT_ISSUE_PROVIDERS = [
        ("simple_issue_provider", "Simple Issue Provider", "plugins.project_snapshot_export.exports.SimpleIssueProvider"),  # noqa: E501
    ]

    return settings

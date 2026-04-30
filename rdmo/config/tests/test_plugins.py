from importlib import metadata

import pytest

from django.core.exceptions import ValidationError

from rdmo.config.constants import PLUGIN_TYPES
from rdmo.config.models import Plugin
from rdmo.config.utils import get_plugins_from_settings
from rdmo.config.validators import PluginURLNameValidator
from rdmo.core.utils import get_model_field_meta
from rdmo.options.providers import Provider
from rdmo.projects.exports import Export
from rdmo.projects.imports import Import
from rdmo.projects.models import Project
from rdmo.projects.providers import IssueProvider


def test_get_plugin_types_from_internal_plugins():
    assert Export.plugin_type == PLUGIN_TYPES.PROJECT_EXPORT
    assert Import.plugin_type == PLUGIN_TYPES.PROJECT_IMPORT
    assert IssueProvider.plugin_type == PLUGIN_TYPES.PROJECT_ISSUE_PROVIDER
    assert Provider.plugin_type == PLUGIN_TYPES.OPTIONSET_PROVIDER

@pytest.mark.django_db
def test_plugin_create_and_render():
    # Arrange: create the Plugin model instance
    project = Project.objects.get(id=1)
    instance = Plugin.objects.create(
        uri_prefix="https://example.org/terms",
        uri_path="test-plugins-export",
        python_path="plugins.project_export.exports.SimpleExportPlugin",
        title_lang1="Test Export Plugin",
        title_lang2="Test Export Plugin(lang2)",
        available=True,
        plugin_settings={"foo": "bar"},
    )

    # get class and initialize like a legacy style plugin
    export_plugin = instance.initialize_class()
    export_plugin.project = project
    export_plugin.snapshot = None
    # Call export (render) and assert behavior
    assert instance.plugin_type == PLUGIN_TYPES.PROJECT_EXPORT
    response = export_plugin.render()
    assert response.status_code == 200
    text = response.content.decode()
    assert text,"response of test export plugin is empty"


@pytest.mark.django_db
def test_plugin_save_sets_issue_provider_type():
    instance = Plugin.objects.create(
        uri_prefix="https://example.org/terms",
        uri_path="test-plugins-issue-provider",
        python_path="plugins.project_issue_providers.providers.SimpleIssueProvider",
        title_lang1="Test Issue Provider",
        title_lang2="Test Issue Provider(lang2)",
        available=True,
        plugin_settings={"foo": "bar"},
    )

    plugin = Plugin.objects.get(pk=instance.pk)
    assert plugin.plugin_type == PLUGIN_TYPES.PROJECT_ISSUE_PROVIDER

def test_get_plugins_from_settings_uses_default_uri_prefix(settings):

    plugins = get_plugins_from_settings()
    for plugin in plugins:
        if plugin['python_path'].startswith('plugins.'):
            assert plugin["uri_prefix"] == "https://rdmorganiser.github.io/terms"


def test_get_model_field_meta_serializes_plugin_python_path_choices(settings):
    settings.PLUGINS = [
        'rdmo.projects.exports.RDMOXMLExport',
        'plugins.project_export.exports.SimpleExportPlugin',
    ]

    meta = get_model_field_meta(Plugin)

    assert meta['python_path']['choices'] == [
        ('rdmo.projects.exports.RDMOXMLExport', 'rdmo.projects.exports.RDMOXMLExport'),
        ('plugins.project_export.exports.SimpleExportPlugin', 'plugins.project_export.exports.SimpleExportPlugin'),
    ]

def test_build_plugin_meta_includes_distribution_version(settings, monkeypatch):
    monkeypatch.setattr('rdmo.config.models.PLUGIN_META_ATTRIBUTES', ('distribution_name', 'distribution_version'))

    class MockPlugin:
        __module__ = 'mocked_package.plugin'

    monkeypatch.setattr(
        metadata,
        'packages_distributions',
        lambda: {'mocked_package': ['mocked-dist']},
    )
    monkeypatch.setattr(metadata, 'version', lambda name: '0.0.1')

    plugin = Plugin()
    assert plugin.build_plugin_meta(MockPlugin) == {'distribution_name': 'mocked-dist', 'distribution_version': '0.0.1'}


def test_plugin_url_name_validator_allows_upload_import_without_url_name(monkeypatch):
    class MockUploadImport:
        plugin_type = PLUGIN_TYPES.PROJECT_IMPORT
        upload = True

    monkeypatch.setattr('rdmo.config.validators.import_string', lambda _: MockUploadImport)

    PluginURLNameValidator()({
        'plugin_type': PLUGIN_TYPES.PROJECT_IMPORT,
        'python_path': 'mocked.upload.import',
    })


def test_plugin_url_name_validator_allows_import_class_url_name(monkeypatch):
    class MockImport:
        plugin_type = PLUGIN_TYPES.PROJECT_IMPORT
        upload = False
        url_name = 'mocked-import'

    monkeypatch.setattr('rdmo.config.validators.import_string', lambda _: MockImport)

    PluginURLNameValidator()({
        'plugin_type': PLUGIN_TYPES.PROJECT_IMPORT,
        'python_path': 'mocked.import',
    })


def test_plugin_url_name_validator_requires_url_name_for_export(monkeypatch):
    class MockExport:
        plugin_type = PLUGIN_TYPES.PROJECT_EXPORT
        url_name = ''

    monkeypatch.setattr('rdmo.config.validators.import_string', lambda _: MockExport)

    with pytest.raises(ValidationError):
        PluginURLNameValidator()({
            'plugin_type': PLUGIN_TYPES.PROJECT_EXPORT,
            'python_path': 'mocked.export',
        })

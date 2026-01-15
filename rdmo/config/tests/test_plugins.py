from importlib import metadata

import pytest

from rdmo.config.constants import PLUGIN_TYPES
from rdmo.config.models import Plugin
from rdmo.config.utils import get_plugin_type_from_class, get_plugins_from_settings
from rdmo.options.providers import Provider
from rdmo.projects.exports import Export
from rdmo.projects.imports import Import
from rdmo.projects.models import Project
from rdmo.projects.providers import IssueProvider


def test_get_plugin_types_from_internal_plugins():
    assert get_plugin_type_from_class(Export) == PLUGIN_TYPES.PROJECT_EXPORT
    assert get_plugin_type_from_class(Import) == PLUGIN_TYPES.PROJECT_IMPORT
    assert get_plugin_type_from_class(IssueProvider) == PLUGIN_TYPES.PROJECT_ISSUE_PROVIDER
    assert get_plugin_type_from_class(Provider) == PLUGIN_TYPES.OPTIONSET_PROVIDER

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

def test_build_plugin_meta_includes_distribution_version(settings, monkeypatch):
    settings.PLUGIN_META_ATTRIBUTES = ('distribution_name', 'distribution_version')

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

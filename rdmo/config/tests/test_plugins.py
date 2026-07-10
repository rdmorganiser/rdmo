from importlib import metadata

import pytest

from django.core.exceptions import ValidationError

from rdmo.config.constants import PLUGIN_TYPES
from rdmo.config.models import Plugin
from rdmo.config.serializers.v1 import PluginSerializer
from rdmo.config.utils import get_plugins_from_settings
from rdmo.config.validators import PluginURLNameValidator
from rdmo.core.utils import get_model_field_meta
from rdmo.options.providers import Provider
from rdmo.projects.exports import Export
from rdmo.projects.imports import Import
from rdmo.projects.models import Project
from rdmo.projects.providers import IssueProvider


class CustomInitExport(Export):
    url_name = 'custom-init-export'

    def __init__(self):
        self.initialized = True


class LegacyExport(Export):

    def __init__(self, key, label, python_path):
        self.key = key
        self.label = label
        self.python_path = python_path


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


@pytest.mark.django_db
def test_plugin_settings_resolution_order(settings):
    settings.SIMPLE_IMPORT_PLUGIN = {
        'API_URL': 'https://django.example.org/api',
        'CLIENT_SECRET': 'django-secret',
    }
    plugin_settings = {
        'API_URL': 'https://plugin.example.org/api',
    }
    instance = Plugin.objects.create(
        uri_prefix="https://example.org/terms",
        uri_path="test-simple-import-plugin",
        python_path="plugins.project_import.imports.SimpleImportPlugin",
        title_lang1="Test Simple Import Plugin",
        plugin_settings=plugin_settings,
    )

    plugin = instance.initialize_class()

    assert plugin.plugin == instance
    assert plugin.plugin_settings == plugin_settings
    assert plugin.plugin_metadata == instance.plugin_meta
    assert plugin.settings.API_URL == 'https://plugin.example.org/api'
    assert plugin.settings.CLIENT_SECRET == 'django-secret'
    assert plugin.settings.DEFAULT_VALUE == 'default'
    assert plugin.settings.TIMEOUT == 10


@pytest.mark.django_db
def test_plugin_settings_form_restricts_settings_names():
    instance = Plugin(
        uri_prefix="https://example.org/terms",
        uri_path="test-simple-import-plugin",
        python_path="plugins.project_import.imports.SimpleImportPlugin",
        title_lang1="Test Simple Import Plugin",
        plugin_settings={
            'API_URL': 'https://plugin.example.org/api',
            'CLIENT_SECRET': 'plugin-secret',
            'UNKNOWN_SETTING': 'invalid',
        },
    )

    with pytest.raises(ValidationError) as excinfo:
        instance.full_clean()

    assert 'Unknown plugin setting(s): UNKNOWN_SETTING' in excinfo.value.message_dict['plugin_settings']


@pytest.mark.django_db
def test_plugin_settings_form_validates_missing_required_settings(settings):
    settings.SIMPLE_IMPORT_PLUGIN = {}
    instance = Plugin(
        uri_prefix="https://example.org/terms",
        uri_path="test-simple-import-plugin",
        python_path="plugins.project_import.imports.SimpleImportPlugin",
        title_lang1="Test Simple Import Plugin",
        plugin_settings={
            'API_URL': 'https://plugin.example.org/api',
        },
    )

    with pytest.raises(ValidationError) as excinfo:
        instance.full_clean()

    assert any(
        'CLIENT_SECRET' in message
        for message in excinfo.value.message_dict['plugin_settings']
    )


@pytest.mark.django_db
def test_plugin_settings_without_form_remain_flexible():
    instance = Plugin(
        uri_prefix="https://example.org/terms",
        uri_path="test-custom-init-export",
        python_path="rdmo.config.tests.test_plugins.CustomInitExport",
        title_lang1="Test Custom Init Export",
        plugin_settings=['not', 'an', 'object'],
    )

    instance.full_clean()


@pytest.mark.django_db
def test_plugin_settings_form_requires_settings_namespace_for_django_settings(settings):
    settings.CLIENT_SECRET = 'django-secret'
    settings.TIMEOUT = 99
    instance = Plugin.objects.create(
        uri_prefix="https://example.org/terms",
        uri_path="test-simple-import-plugin",
        python_path="plugins.project_import.imports.SimpleImportPlugin",
        title_lang1="Test Simple Import Plugin",
        plugin_settings={
            'API_URL': 'https://plugin.example.org/api',
            'CLIENT_SECRET': 'plugin-secret',
        },
    )

    plugin = instance.initialize_class()

    assert plugin.settings.CLIENT_SECRET == 'plugin-secret'
    assert plugin.settings.TIMEOUT == 10


@pytest.mark.django_db
def test_plugin_settings_fall_back_to_flat_namespaced_django_settings(settings):
    settings.SIMPLE_IMPORT_PLUGIN = {}
    settings.SIMPLE_IMPORT_PLUGIN_API_URL = 'https://django.example.org/api'
    settings.SIMPLE_IMPORT_PLUGIN_CLIENT_SECRET = 'django-secret'
    instance = Plugin.objects.create(
        uri_prefix="https://example.org/terms",
        uri_path="test-flat-simple-import-plugin",
        python_path="plugins.project_import.imports.SimpleImportPlugin",
        title_lang1="Test Flat Simple Import Plugin",
    )

    plugin = instance.initialize_class()

    assert plugin.settings.API_URL == 'https://django.example.org/api'
    assert plugin.settings.CLIENT_SECRET == 'django-secret'
    assert plugin.settings.DEFAULT_VALUE == 'default'


@pytest.mark.django_db
def test_plugin_settings_without_form_support_namespaced_django_settings(settings):
    settings.SIMPLE_EXPORT_PLUGIN = {
        'CLIENT_SECRET': 'django-secret',
    }
    settings.SECRET_PLUGIN_VALUE = 'secret'
    instance = Plugin.objects.create(
        uri_prefix="https://example.org/terms",
        uri_path="test-simple-export-plugin",
        python_path="plugins.project_export.exports.SimpleExportPlugin",
        title_lang1="Test Simple Export Plugin",
        plugin_settings={
            'API_URL': 'https://plugin.example.org/api',
        },
    )

    plugin = instance.initialize_class()

    assert plugin.settings.API_URL == 'https://plugin.example.org/api'
    assert plugin.settings.CLIENT_SECRET == 'django-secret'
    assert plugin.settings.TIMEOUT == 10

    setting_name = 'SECRET_PLUGIN_VALUE'
    with pytest.raises(AttributeError):
        getattr(plugin.settings, setting_name)


@pytest.mark.django_db
def test_plugin_serializer_validates_settings_form(settings):
    python_path = "plugins.project_import.imports.SimpleImportPlugin"
    settings.PLUGINS = [python_path]
    serializer = PluginSerializer(data={
        'uri_prefix': "https://example.org/terms",
        'uri_path': "test-simple-import-plugin",
        'python_path': python_path,
        'plugin_settings': {
            'API_URL': 'https://plugin.example.org/api',
            'CLIENT_SECRET': 'plugin-secret',
            'UNKNOWN_SETTING': 'invalid',
        },
        'title_en': "Test Simple Import Plugin",
        'title_de': "Test Simple Import Plugin",
        'help_en': "",
        'help_de': "",
    })
    serializer.fields['python_path'].choices = [(python_path, python_path)]

    assert serializer.is_valid() is False
    assert 'plugin_settings' in serializer.errors


@pytest.mark.django_db
def test_initialize_class_supports_settings_form_on_optionset_provider():
    instance = Plugin.objects.create(
        uri_prefix="https://example.org/terms",
        uri_path="test-simple-optionset-provider",
        python_path="plugins.optionset_providers.providers.SimpleOptionSetProvider",
        title_lang1="Test Simple Option Set Provider",
        plugin_settings={'PROVIDER_LABEL': 'Provider label'},
    )

    plugin = instance.initialize_class()

    assert instance.plugin_type == PLUGIN_TYPES.OPTIONSET_PROVIDER
    assert instance.plugin_meta['search'] is False
    assert instance.plugin_meta['refresh'] is True
    assert plugin.plugin == instance
    assert plugin.settings.PROVIDER_LABEL == 'Provider label'
    assert plugin.get_options(project=None)[0] == {
        'id': 'simple_1',
        'text': 'Provider label',
        'help': 'One'
    }


@pytest.mark.django_db
def test_initialize_class_attaches_plugin_to_custom_init_plugin():
    instance = Plugin.objects.create(
        uri_prefix="https://example.org/terms",
        uri_path="test-custom-init-export",
        python_path="rdmo.config.tests.test_plugins.CustomInitExport",
        title_lang1="Test Custom Init Export",
        plugin_settings={'TEST_PLUGIN_ONLY': 'plugin'},
    )

    plugin = instance.initialize_class()

    assert plugin.initialized is True
    assert plugin.plugin == instance
    assert plugin.plugin_settings == {'TEST_PLUGIN_ONLY': 'plugin'}


@pytest.mark.django_db
def test_initialize_class_rejects_legacy_signature():
    instance = Plugin(
        uri_prefix="https://example.org/terms",
        uri_path="test-legacy-export",
        python_path="rdmo.config.tests.test_plugins.LegacyExport",
        title_lang1="Test Legacy Export",
        url_name="legacy-export",
        plugin_settings={'TEST_PLUGIN_ONLY': 'plugin'},
    )

    with pytest.raises(ValueError, match='Could not initialize class'):
        instance.initialize_class()


@pytest.mark.django_db
def test_filter_plugins_for_project_filters_by_url_name_and_orders(settings):
    settings.PLUGINS = [
        'rdmo.projects.exports.RDMOXMLExport',
        'plugins.project_export.exports.SimpleExportPlugin',
    ]
    project = Project.objects.get(id=1)
    Plugin.objects.create(
        uri_prefix="https://example.org/terms",
        uri_path="test-plugins-export-late",
        python_path="plugins.project_export.exports.SimpleExportPlugin",
        title_lang1="Test Export Plugin",
        available=True,
        url_name="shared",
        order=2,
    )
    Plugin.objects.create(
        uri_prefix="https://example.org/terms",
        uri_path="test-plugins-export-early",
        python_path="rdmo.projects.exports.RDMOXMLExport",
        title_lang1="RDMO XML",
        available=True,
        url_name="shared",
        order=1,
    )

    plugins = Plugin.objects.filter_plugins_for_project(
        project=project,
        plugin_type=PLUGIN_TYPES.PROJECT_EXPORT,
        url_name="shared",
    )

    assert list(plugins.values_list('order', flat=True)) == [1, 2]


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

import importlib

import pytest

from rdmo.config.models import Plugin


@pytest.fixture
def enable_plugins(settings):
    settings.INSTALLED_APPS += [
        "rdmo.testing.plugins.export_plugin",
        "rdmo.testing.plugins.import_plugin",
        "rdmo.testing.plugins.optionset_provider",
    ]
    # also insert into the relevant plugin-tuples in settings,
    # e.g. PROJECT_EXPORTS, PROJECT_IMPORTS, OPTIONSET_PROVIDERS
    # you need to mirror what your PR expects; for example:
    settings.PROJECT_EXPORTS = list(getattr(settings, "PROJECT_EXPORTS", []))
    settings.PROJECT_EXPORTS.append(
        ("test_export", "Test Export", "rdmo.testing.plugins.export_plugin.plugin.TestExportPlugin")
    )
    settings.PROJECT_IMPORTS = list(getattr(settings, "PROJECT_IMPORTS", []))
    settings.PROJECT_IMPORTS.append(
        ("test_import", "Test Import", "rdmo.testing.plugins.import_plugin.plugin.TestImportPlugin")
    )
    settings.OPTIONSET_PROVIDERS = list(getattr(settings, "OPTIONSET_PROVIDERS", []))
    settings.OPTIONSET_PROVIDERS.append(
        ("test_optionset", "Test OptionSet", "rdmo.testing.plugins.optionset_provider.plugin.TestOptionSetProvider")
    )
    return settings


@pytest.mark.django_db
def test_export_plugins(enable_plugins):
    # Create the Plugin model instance linking to your dummy export plugin
    plugin = Plugin.objects.create(
        uri_prefix="https://example.org",
        uri_path="test-export",
        python_path="rdmo.testing.plugins.export_plugin.plugin.TestExportPlugin",
        title_lang1="Test Export Plugin",
        available=True,
        plugin_settings={"foo": "bar"},
    )

    # Check uri built correctly
    assert plugin.uri == "https://example.org/plugins/test-export"

    # Dynamically import via importlib
    module_name, class_name = plugin.python_path.rsplit(".", 1)
    mod = importlib.import_module(module_name)
    cls = getattr(mod, class_name)
    instance = cls()

    # Call export (render) and assert behavior
    response = instance.render()
    text = response.content.decode()
    assert "Exported project" in text  # depends on your dummy plugin

    # You can also test that this plugin is present in settings.PROJECT_EXPORTS
    found = [t for t in enable_plugins.PROJECT_EXPORTS if t[0] == "test_export"]
    assert found, "test_export not found in PROJECT_EXPORTS"
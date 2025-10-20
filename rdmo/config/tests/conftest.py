import pytest


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

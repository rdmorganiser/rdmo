import pytest


@pytest.fixture
def enable_plugins(settings):
    settings.INSTALLED_APPS += [
        "plugins.export_plugin",
        "plugins.import_plugin",
        "plugins.optionset_provider_plugin",
    ]
    # also insert into the relevant plugin-tuples in settings,
    # e.g. PROJECT_EXPORTS, PROJECT_IMPORTS, OPTIONSET_PROVIDERS
    # to support the backwards compatible settings
    settings.PROJECT_EXPORTS = list(getattr(settings, "PROJECT_EXPORTS", []))
    settings.PROJECT_EXPORTS.append(
        ("test_export", "Test Export", "plugins.export_plugin.plugin.TestExportPlugin")
    )
    settings.PROJECT_IMPORTS = list(getattr(settings, "PROJECT_IMPORTS", []))
    settings.PROJECT_IMPORTS.append(
        ("test_import", "Test Import", "plugins.import_plugin.plugin.TestImportPlugin")
    )
    settings.OPTIONSET_PROVIDERS = list(getattr(settings, "OPTIONSET_PROVIDERS", []))
    settings.OPTIONSET_PROVIDERS.append(
        ("test_optionset", "Test OptionSet", "plugins.optionset_provider_plugin.plugin.TestOptionSetProvider")
    )
    return settings

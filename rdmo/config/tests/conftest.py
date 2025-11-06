
#
# @pytest.fixture
# def enable_plugins(settings):
#     settings.INSTALLED_APPS += [
#         "plugins",
#     ]
#     # # insert the relevant legacy plugin-tuples in settings,
#     # # e.g. PROJECT_EXPORTS, PROJECT_IMPORTS, OPTIONSET_PROVIDERS
#     # # to support the backwards compatible settings
#     # settings.PROJECT_EXPORTS = list(getattr(settings, "PROJECT_EXPORTS", []))
#     # settings.PROJECT_EXPORTS.append(
#     #     ("test_export", "Test Export", "plugins.project_export.exports.SimpleExportPlugin")
#     # )
#     # settings.PROJECT_SNAPSHOT_EXPORTS = list(getattr(settings, "PROJECT_SNAPSHOT_EXPORTS", []))
#     # settings.PROJECT_SNAPSHOT_EXPORTS.append(
#     #     ("test_export", "Test Export", "plugins.project_snapshot_export.exports.SimpleSnapshotExportPlugin")
#     # )
#     #
#     # settings.PROJECT_IMPORTS = list(getattr(settings, "PROJECT_IMPORTS", []))
#     # settings.PROJECT_IMPORTS.append(
#     #     ("test_import", "Test Import", "plugins.project_import.imports.TestImportPlugin")
#     # )
#     # settings.OPTIONSET_PROVIDERS = list(getattr(settings, "OPTIONSET_PROVIDERS", []))
#     # settings.OPTIONSET_PROVIDERS.append(
#     #     ("test_optionset", "Test OptionSet", "plugins.optionset_providers.providers.SimpleProvider")
#     # )
#     # settings.PROJECT_ISSUE_PROVIDERS = list(getattr(settings, "PROJECT_ISSUE_PROVIDERS", []))
#     # settings.PROJECT_ISSUE_PROVIDERS.append(
#     #     ("test_optionset", "Test OptionSet", "plugins.project_snapshot_export.exports.SimpleIssueProvider")
#     # )
#
#     return settings

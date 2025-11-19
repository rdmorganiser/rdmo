
from django.core.checks import Warning

from rdmo.config.checks import deprecated_plugin_settings_check, repr_new_settings

LEGACY_KEYS = [
    "PROJECT_EXPORTS",
    "PROJECT_SNAPSHOT_EXPORTS",
    "PROJECT_IMPORTS",
    "PROJECT_ISSUE_PROVIDERS",
    "PROJECT_IMPORTS_LIST",
    "OPTIONSET_PROVIDERS",
]


def _clear_legacy_settings(settings):
    """
    Helper to make sure none of the legacy settings are set.
    This keeps the tests independent from the global test settings.
    """
    for key in [*LEGACY_KEYS, "PLUGINS"]:
        if hasattr(settings, key):
            delattr(settings, key)


def test_deprecated_plugin_settings_no_legacy_returns_empty(settings):
    """
    When no legacy plugin settings are defined, the check must be silent.
    """
    _clear_legacy_settings(settings)

    issues = deprecated_plugin_settings_check(app_configs=None)

    assert issues == []


def test_deprecated_plugin_settings_with_legacy_only(enable_legacy_plugins, settings):
    """
    With only legacy settings configured, we expect a single W001 warning
    and a hint that includes the PLUGINS example with python paths.
    """
    # make sure PLUGINS is not set
    if hasattr(settings, "PLUGINS"):
        delattr(settings, "PLUGINS")

    issues = deprecated_plugin_settings_check(app_configs=None)

    assert len(issues) == 1
    issue = issues[0]

    assert isinstance(issue, Warning)
    assert issue.id == "rdmo.config.W001"

    # the message mentions the deprecated keys
    assert "deprecated as of RDMO 2.5.0" in issue.msg
    assert "PROJECT_EXPORTS" in issue.msg

    # the hint uses repr_new_settings(...) and should contain python paths
    # from the legacy tuples defined in enable_legacy_plugins
    assert "PLUGINS" in issue.hint
    assert "plugins.project_export.exports.SimpleExportPlugin" in issue.hint


def test_deprecated_plugin_settings_with_legacy_and_plugins(enable_legacy_plugins, settings):
    """
    If legacy settings AND PLUGINS are set, we expect W001 + W002.
    """
    # PLUGINS exists in addition to the legacy settings
    settings.PLUGINS = ["plugins.project_export.exports.SimpleExportPlugin"]

    issues = deprecated_plugin_settings_check(app_configs=None)

    ids = {issue.id for issue in issues}
    assert ids == {"rdmo.config.W001", "rdmo.config.W002"}

    w2 = next(i for i in issues if i.id == "rdmo.config.W002")
    assert "ignored" in w2.msg.lower()
    assert "Remove the following legacy settings" in w2.hint


def test_repr_new_settings_formats_single_and_multiple_paths():
    """
    repr_new_settings should produce a sensible PLUGINS example
    for 0, 1 and multiple python paths.
    """
    assert repr_new_settings(set()) == ""

    single = repr_new_settings({"a.b.Class"})
    assert "PLUGINS" in single
    assert "a.b.Class" in single

    multi = repr_new_settings({"a.b.Class", "c.d.Other"})
    # multi-line list with both paths present
    assert "PLUGINS" in multi
    assert "a.b.Class" in multi
    assert "c.d.Other" in multi

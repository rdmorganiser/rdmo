from collections import defaultdict

from django.core.checks import Warning, register


@register()
def deprecated_plugin_settings_check(app_configs, **kwargs):
    from django.conf import settings
    legacy_settings = [
        "PROJECT_EXPORTS",
        "PROJECT_SNAPSHOT_EXPORTS",
        "PROJECT_IMPORTS",
        "PROJECT_ISSUE_PROVIDERS",
        "PROJECT_IMPORTS_LIST",
        "OPTIONSET_PROVIDERS",
    ]
    issues = []
    legacy_settings_used_keys = {
        i for i in legacy_settings if hasattr(settings, i)
    }
    if legacy_settings_used_keys:
        _verb = "are" if len(legacy_settings_used_keys) > 1 else "is"
        legacy_settings = {
            i: getattr(settings, i) for i in legacy_settings_used_keys
        }
        _legacy_settings_plugins = defaultdict(list)
        for name,entries in legacy_settings.items():
            for entry in entries:
                _legacy_settings_plugins[name].append(entry)
        issues.append(Warning(
            f"{', '.join(legacy_settings_used_keys)} {_verb} deprecated as of RDMO 2.5.0; "
            f"use PLUGINS = ['python.dotted.paths', ...] instead.",
            id="rdmo.config.W001",
            hint="Define the legacy plugin settings in PLUGINS and remove the legacy settings.",
        ))
        # If both PLUGINS and any legacy key exist
        if hasattr(settings, "PLUGINS"):
            issues.append(Warning(
                "PLUGINS is set; legacy settings are ignored.",
                id="rdmo.config.W002",
                hint=f"Remove legacy settings {', '.join(legacy_settings_used_keys)} to avoid confusion.",
            ))
    return issues

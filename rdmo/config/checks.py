from django.core.checks import Warning, register


@register()
def deprecated_plugin_settings_check(app_configs, **kwargs):
    from django.conf import settings
    legacy = [
        "PROJECT_EXPORTS",
        "PROJECT_SNAPSHOT_EXPORTS",
        "PROJECT_IMPORTS",
        "PROJECT_ISSUE_PROVIDERS",
        "PROJECT_IMPORTS_LIST",
        "OPTIONSET_PROVIDERS",
    ]
    issues = []
    legacy_settings_used = set()
    for key in legacy:
        if hasattr(settings, key):
            legacy_settings_used.add(key)
    if legacy_settings_used:
        _verb = "are" if len(legacy_settings_used) > 1 else "is"
        issues.append(Warning(
            f"{','.join(legacy_settings_used)} {_verb} deprecated as of RDMO 2.5.0; "
            f"use PLUGINS = [python.dotted.paths,..] instead.",
            id="rdmo.config.W001",
            hint="Move class paths or feature toggles into PLUGINS and remove the legacy key.",
        ))
    # If both PLUGINS and any legacy key exist
    if hasattr(settings, "PLUGINS") and any(hasattr(settings, k) for k in legacy):
        issues.append(Warning(
            "PLUGINS is set; legacy settings are ignored.",
            id="rdmo.config.W002",
            hint="Remove legacy keys to avoid confusion.",
        ))
    return issues

import importlib

import pytest

from rdmo.config.models import Plugin


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

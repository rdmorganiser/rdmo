import pytest

from rdmo.config.models import Plugin
from rdmo.projects.models import Project


@pytest.mark.django_db
def test_plugin_create_and_render(enable_plugins, settings):
    # Arrange: create the Plugin model instance
    settings.LANGUAGE_CODE = 'en'
    project = Project.objects.get(id=1)
    instance = Plugin.objects.create(
        uri_prefix="https://example.org/terms",
        uri_path="test-plugins-export",
        python_path="plugins.export_plugin.plugin.TestExportPlugin",
        title_lang1="Test Export Plugin",
        available=True,
        plugin_settings={"foo": "bar"},
    )

    # get class and initialize like a legacy style plugin
    export_plugin = instance.initialize_class()
    export_plugin.project = project
    export_plugin.snapshot = None
    # Call export (render) and assert behavior
    response = export_plugin.render()
    assert response.status_code == 200
    text = response.content.decode()
    assert text,"response of test export plugin is empty"

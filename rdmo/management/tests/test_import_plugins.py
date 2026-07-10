import json
from pathlib import Path

from rdmo.config.models import Plugin

from .helpers_import_elements import (
    parse_xml_and_import_elements,
)


def test_create_plugins(db, settings):
    Plugin.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'plugins.xml'
    _, root, imported_elements = parse_xml_and_import_elements(xml_file)

    assert len(root) == len(imported_elements) == Plugin.objects.count() == 2
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)

    plugin = Plugin.objects.get(uri="https://example.com/terms/plugins/simple-export-plugin")
    assert plugin.uri_prefix == "https://example.com/terms"
    assert plugin.uri_path == "simple-export-plugin"
    assert plugin.comment == "Example export plugin imported via XML"
    assert plugin.title_lang1 == "Example Export Plugin"
    assert plugin.title_lang2 == "Beispiel Export Plugin"
    assert plugin.python_path == "plugins.project_export.exports.SimpleExportPlugin"
    plugin_settings = plugin.plugin_settings
    if isinstance(plugin_settings, str):
        plugin_settings = json.loads(plugin_settings)
    assert plugin_settings["token"] == "abc123"

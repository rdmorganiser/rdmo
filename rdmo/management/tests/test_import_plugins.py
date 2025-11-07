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

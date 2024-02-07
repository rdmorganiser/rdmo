from pathlib import Path

from rdmo.conditions.models import Condition
from rdmo.core.xml import convert_elements, flat_xml_to_elements, order_elements, read_xml_file
from rdmo.management.imports import import_elements


def test_create_conditions(db, settings):
    Condition.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'conditions.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == len(elements) == Condition.objects.count() == 15
    assert all(element['created'] is True for element in elements)
    assert all(element['updated'] is False for element in elements)


def test_update_conditions(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'conditions.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == len(elements)
    assert all(element['created'] is False for element in elements)
    assert all(element['updated'] is True for element in elements)


def test_create_legacy_conditions(db, settings):
    Condition.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'conditions.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == len(elements) == Condition.objects.count() == 15
    assert all(element['created'] is True for element in elements)
    assert all(element['updated'] is False for element in elements)


def test_update_legacy_conditions(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'conditions.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == len(elements) == 15
    assert all(element['created'] is False for element in elements)
    assert all(element['updated'] is True for element in elements)

from pathlib import Path

from rdmo.core.xml import convert_elements, flat_xml_to_elements, order_elements, read_xml_file
from rdmo.management.imports import import_elements
from rdmo.options.models import Option, OptionSet


def test_create_optionsets(db, settings):
    OptionSet.objects.all().delete()
    Option.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'optionsets.xml'
    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    parsed_elements = elements.values()
    imported_elements = import_elements(parsed_elements)

    assert len(root) == len(elements) == len(imported_elements) == 13
    assert OptionSet.objects.count() == 4
    assert Option.objects.count() == 9
    assert all(element['created'] is True for element in parsed_elements)
    assert all(element['updated'] is False for element in parsed_elements)


def test_update_optionsets(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'optionsets.xml'
    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    parsed_elements = elements.values()
    imported_elements = import_elements(parsed_elements)

    assert len(root) == len(elements) == len(imported_elements) == 13
    assert all(element['created'] is False for element in parsed_elements)
    assert all(element['updated'] is True for element in parsed_elements)


def test_create_options(db, settings):
    Option.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'options.xml'
    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    parsed_elements = elements.values()
    imported_elements = import_elements(parsed_elements)

    assert len(root) == len(elements) == len(imported_elements) == Option.objects.count() == 9
    assert all(element['created'] is True for element in parsed_elements)
    assert all(element['updated'] is False for element in parsed_elements)


def test_update_options(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'options.xml'
    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    parsed_elements = elements.values()
    imported_elements = import_elements(parsed_elements)

    assert len(root) == len(elements) == len(imported_elements) == 9
    assert all(element['created'] is False for element in parsed_elements)
    assert all(element['updated'] is True for element in parsed_elements)


def test_create_legacy_options(db, settings):
    OptionSet.objects.all().delete()
    Option.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'options.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    parsed_elements = elements.values()
    imported_elements = import_elements(parsed_elements)

    assert len(root) == len(elements) == len(imported_elements) == 12
    assert OptionSet.objects.count() == 4
    assert Option.objects.count() == 8
    assert all(element['created'] is True for element in parsed_elements)
    assert all(element['updated'] is False for element in parsed_elements)


def test_update_legacy_options(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'options.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    parsed_elements = elements.values()
    imported_elements = import_elements(parsed_elements)

    assert len(root) == len(elements) == len(imported_elements) == 12
    assert all(element['created'] is False for element in parsed_elements)
    assert all(element['updated'] is True for element in parsed_elements)

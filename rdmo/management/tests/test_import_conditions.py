from pathlib import Path

from rdmo.conditions.models import Condition
from rdmo.management.imports import import_elements

from . import change_fields_elements, read_xml_and_parse_to_elements


def test_create_conditions(db, settings):
    Condition.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'conditions.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == Condition.objects.count() == 15
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_conditions(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'conditions.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 15
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


def test_update_conditions_with_changed_comments(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'conditions.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    elements, changed_elements = change_fields_elements(elements, n=3)
    # breakpoint()
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 15
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len([i for i in elements if i['updated_and_changed']]) == len(changed_elements)


def test_create_legacy_conditions(db, settings):
    Condition.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'conditions.xml'
    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == Condition.objects.count() == 15
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_legacy_conditions(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'conditions.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 15
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)

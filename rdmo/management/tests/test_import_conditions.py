from pathlib import Path

import pytest

from rdmo.conditions.models import Condition
from rdmo.management.imports import import_elements

from .helpers_import_elements import (
    _test_helper_change_fields_elements,
    _test_helper_filter_updated_and_changed,
)
from .helpers_xml import read_xml_and_parse_to_elements

imported_update_changes = [
    None,
    {
    'target_text' : 'test target_text {}',
    'relation': 'notempty'
    }
]

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


@pytest.mark.parametrize('update_dict', imported_update_changes)
def test_update_conditions_with_changed_fields(db, settings, update_dict):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'conditions.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    elements, changed_elements = _test_helper_change_fields_elements(elements, update_dict=update_dict, n=7)
    imported_elements = import_elements(elements)
    imported_and_changed = _test_helper_filter_updated_and_changed(imported_elements)
    assert len(root) == len(imported_elements) == 15
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
        assert test['updated_and_changed'] == imported['updated_and_changed']


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

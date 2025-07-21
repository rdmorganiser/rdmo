from pathlib import Path

import pytest

from rdmo.core.imports import ImportElementFields
from rdmo.domain.models import Attribute
from rdmo.management.imports import import_elements

from .helpers_import_elements import (
    _test_helper_change_fields_elements,
    _test_helper_filter_updated_and_changed,
    parse_xml_and_import_elements,
)
from .helpers_xml import read_xml_and_parse_to_root_and_elements

fields_to_be_changed = (('comment',),)

def test_create_domain(db, settings):
    Attribute.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'attributes.xml'

    elements, root, imported_elements = parse_xml_and_import_elements(xml_file)

    assert len(root) == len(imported_elements) == Attribute.objects.count() == 86
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_domain(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'attributes.xml'

    elements, root, imported_elements = parse_xml_and_import_elements(xml_file)

    assert len(root) == len(imported_elements)
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


@pytest.mark.parametrize('updated_fields', fields_to_be_changed)
def test_update_attributes_with_changed_fields(db, settings, updated_fields):
    _change_count = Attribute.objects.count() / 2
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'attributes.xml'
    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    # import initial elements from xml
    _el = import_elements(elements, save=True)
    # update the elements and call import again
    updated_elements = _test_helper_change_fields_elements(elements, fields_to_update=updated_fields, n=_change_count)
    changed_elements = _test_helper_filter_updated_and_changed(updated_elements.values(), updated_fields=updated_fields)
    imported_elements = import_elements(updated_elements)
    imported_and_changed = _test_helper_filter_updated_and_changed(imported_elements, updated_fields=updated_fields)

    assert len(root) == len(imported_elements) == 86
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
       assert test[ImportElementFields.DIFF] == imported[ImportElementFields.DIFF]


def test_create_legacy_domain(db, settings):
    Attribute.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'domain.xml'

    elements, root, imported_elements = parse_xml_and_import_elements(xml_file)

    assert len(root) == len(imported_elements) == 86
    assert Attribute.objects.count() == 86
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_legacy_domain(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'domain.xml'

    elements, root, imported_elements = parse_xml_and_import_elements(xml_file)

    assert len(root) == len(imported_elements) == 86
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)

from pathlib import Path

import pytest

from rdmo.core.imports import ImportElementFields
from rdmo.management.imports import import_elements
from rdmo.tasks.models import Task

from .helpers_import_elements import (
    _test_helper_change_fields_elements,
    _test_helper_filter_updated_and_changed,
)
from .helpers_xml import read_xml_and_parse_to_root_and_elements

fields_to_be_changed = (('comment',),)


def test_create_tasks(db, settings):
    Task.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'tasks.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == Task.objects.count() == 2
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_tasks(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'tasks.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 2
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


@pytest.mark.parametrize('updated_fields', fields_to_be_changed)
def test_update_tasks_with_changed_fields(db, settings, updated_fields):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'tasks.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    elements = _test_helper_change_fields_elements(elements, fields_to_update=updated_fields, n=1)
    changed_elements = _test_helper_filter_updated_and_changed(elements.values(), updated_fields=updated_fields)
    imported_elements = import_elements(elements)
    imported_and_changed = _test_helper_filter_updated_and_changed(imported_elements, updated_fields=updated_fields)
    assert len(root) == len(imported_elements) == 2
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
        assert test[ImportElementFields.DIFF] == imported[ImportElementFields.DIFF]


def test_create_legacy_tasks(db, settings):
    Task.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'tasks.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == Task.objects.count() == 2
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_legacy_tasks(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'tasks.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 2
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)

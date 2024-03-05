import json
from pathlib import Path

import pytest

from rdmo.management.imports import import_elements
from rdmo.options.models import Option, OptionSet

from .helpers_import_elements import (
    _test_helper_change_fields_elements,
    _test_helper_filter_updated_and_changed,
)
from .helpers_models import delete_all_objects
from .helpers_xml import read_xml_and_parse_to_elements

fields_to_be_changed = (('comment',),)

def test_create_optionsets(db, settings):
    delete_all_objects([OptionSet, Option])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'optionsets.xml'
    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(elements) == len(imported_elements) == 13
    assert OptionSet.objects.count() == 4
    assert Option.objects.count() == 9
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_optionsets(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'optionsets.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(elements) == len(imported_elements) == 13
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


@pytest.mark.parametrize('updated_fields', fields_to_be_changed)
def test_update_optionsets_with_changed_fields(db, settings, updated_fields):
    delete_all_objects([OptionSet, Option])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'optionsets.xml'
    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)
    assert len(root) == len(imported_elements) == 13
    # start test with fresh options in db
    _n_change = int(Option.objects.count() / 2)
    elements = _test_helper_change_fields_elements(elements, fields_to_update=updated_fields, n=7)
    changed_elements = _test_helper_filter_updated_and_changed(elements.values(), updated_fields=updated_fields)
    imported_elements = import_elements(elements)
    assert len(root) == len(imported_elements) == 13
    imported_and_changed = _test_helper_filter_updated_and_changed(imported_elements, updated_fields=updated_fields)
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
        assert test['updated_and_changed'] == imported['updated_and_changed']


def test_update_optionsets_from_changed_xml(db, settings):
    # Arrange, start test with fresh options in db
    delete_all_objects([OptionSet, Option])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'optionsets.xml'
    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)
    assert len(root) == len(imported_elements) == 13
    # Act, import from xml that has changes
    xml_file_1 = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'updated-and-changed' / 'optionsets-1.xml'
    elements_1, root_1 = read_xml_and_parse_to_elements(xml_file_1)
    imported_elements_1 = import_elements(elements_1, save=False)

    # Assert, compare with pre-defined json
    json_file_1 = xml_file_1.with_suffix(".json")
    _from_json_imported_elements_1 = json.loads(json_file_1.read_text())

    # assert imported_elements_1 == from_json_imported_elements_1
    changed_elements = [i for i in imported_elements_1 if i['changed']]
    warnings_elements = [i for i in imported_elements_1 if i['warnings']]
    assert len(changed_elements) == 5
    assert len(warnings_elements) == 1

    optionset_uri = "http://example.com/terms/options/one_two_three"
    changed_uris = {i['uri']: i for i in changed_elements}
    assert optionset_uri in changed_uris

    # now save the elements_1
    _imported_elements_1_save = import_elements(elements_1, save=True)
    test_ordered_options = [
        'http://example.com/terms/options/one_two_three/three',
        'http://example.com/terms/options/one_two_three/two',
        'http://example.com/terms/options/one_two_three/one',
    ]
    # get the ordered options (via .optionset_options) for this optionset from the db
    optionset_1 = OptionSet.objects.get(uri=optionset_uri)
    optionset_1_options = optionset_1.optionset_options.order_by('order').values_list('option__uri',flat=True)
    for _test, _db in zip(test_ordered_options, optionset_1_options):
        assert _test == _db

def test_create_options(db, settings):
    Option.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'options.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(elements) == len(imported_elements) == Option.objects.count() == 9
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_options(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'options.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(elements) == len(imported_elements) == 9
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


@pytest.mark.parametrize('updated_fields', fields_to_be_changed)
def test_update_options_with_changed_fields(db, settings, updated_fields):
    delete_all_objects([OptionSet, Option])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'options.xml'
    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)
    assert len(root) == len(imported_elements) == 9
    # start test with fresh options in db
    elements = _test_helper_change_fields_elements(elements, fields_to_update=updated_fields, n=4)
    changed_elements = _test_helper_filter_updated_and_changed(elements.values(), updated_fields=updated_fields)
    imported_elements = import_elements(elements)
    imported_and_changed = _test_helper_filter_updated_and_changed(imported_elements, updated_fields=updated_fields)
    assert len(root) == len(imported_elements) == 9
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
        assert test['updated_and_changed'] == imported['updated_and_changed']




def test_create_legacy_options(db, settings):
    delete_all_objects([OptionSet, Option])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'options.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(elements) == len(imported_elements) == 12
    assert OptionSet.objects.count() == 4
    assert Option.objects.count() == 8
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_legacy_options(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'options.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(elements) == len(imported_elements) == 12
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)

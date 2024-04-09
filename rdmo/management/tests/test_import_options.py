from pathlib import Path

import pytest

from rdmo.core.imports import ELEMENT_DIFF_FIELD_NAME, NEW_DATA_FIELD, CURRENT_DATA_FIELD
from rdmo.management.imports import import_elements
from rdmo.options.models import Option, OptionSet

from .helpers_import_elements import (
    _test_helper_change_fields_elements,
    _test_helper_filter_updated_and_changed,
    get_changed_elements
)
from .helpers_models import delete_all_objects
from .helpers_xml import read_xml_and_parse_to_elements

fields_to_be_changed = (('comment',),)

test_optionset = {
    'original': {
        "uri": "http://example.com/terms/options/one_two_three",
        "options": [
            'http://example.com/terms/options/one_two_three/one',
            'http://example.com/terms/options/one_two_three/two',
            'http://example.com/terms/options/one_two_three/three',
            ],
        },
    }

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
        assert test[ELEMENT_DIFF_FIELD_NAME] == imported[ELEMENT_DIFF_FIELD_NAME]


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
    assert imported_elements_1
    assert [i for i in imported_elements_1 if i[ELEMENT_DIFF_FIELD_NAME]]
    warnings_elements = [i for i in imported_elements_1 if i['warnings']]
    assert len(warnings_elements) == 1

    changed_elements = get_changed_elements(imported_elements_1)

    assert test_optionset['original']['uri'] in changed_elements
    assert len([i for i in  changed_elements.values() if i]) == 5

    # change the order of the options, as in the xml
    optionset_element = [i for i in imported_elements_1 if i['uri'] == test_optionset['original']['uri']][0]
    test_optionset_changed_options = test_optionset['original']['options'][::-1]  # the test changes are simply the reversed order of the options
    assert optionset_element
    assert "options" in optionset_element[ELEMENT_DIFF_FIELD_NAME]
    assert optionset_element[ELEMENT_DIFF_FIELD_NAME]['options'][CURRENT_DATA_FIELD] == test_optionset['original']['options']
    assert optionset_element[ELEMENT_DIFF_FIELD_NAME]['options'][NEW_DATA_FIELD] == test_optionset_changed_options

    # now save the elements_1
    _imported_elements_1_save = import_elements(elements_1, save=True)
    # get the ordered options (via .optionset_options) for this optionset from the db
    optionset_1 = OptionSet.objects.get(uri=test_optionset['original']['uri'])
    optionset_1_options = optionset_1.optionset_options.order_by('order').values_list('option__uri',flat=True)
    for _test, _db in zip(test_optionset_changed_options, optionset_1_options):
        assert _test == _db

    # Import again and test that there are no changes detected
    imported_elements_2 = import_elements(elements_1, save=False)
    changed_elements_2 = get_changed_elements(imported_elements_2)
    assert len(changed_elements_2) == 0
    assert len([i for i in imported_elements_2 if i['warnings']]) == 1


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
        assert test[ELEMENT_DIFF_FIELD_NAME] == imported[ELEMENT_DIFF_FIELD_NAME]




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

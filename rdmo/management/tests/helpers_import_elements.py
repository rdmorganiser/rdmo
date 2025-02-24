import random
from collections import OrderedDict
from functools import partial
from typing import Optional, Union

from rdmo.core.imports import ImportElementFields, track_changes_on_element
from rdmo.management.import_utils import initialize_import_element_dict
from rdmo.management.imports import import_elements
from rdmo.management.tests.helpers_xml import read_xml_and_parse_to_root_and_elements

IMPORT_ELEMENT_PANELS_LOCATOR = ".list-group > .list-group-item > .checkbox"
IMPORT_ELEMENT_PANELS_LOCATOR_SHOWN = ".list-group > .list-group-item > .row"

UPDATE_FIELD_FUNCS = {
    'comment': lambda text: f"this is a test comment {text}",
    'target_text': lambda text: f"test target_text {text}",
    'relation': lambda text: "notempty".format(),
}


def filter_changed_fields(element, updated_fields=None) -> bool:
    _changed = element.get('changed', False)
    if updated_fields is None:
        return _changed
    changes = element.get(ImportElementFields.DIFF, {})
    for field, diff in changes.items():
        if field not in updated_fields:
            continue
        _new_value = diff.get(ImportElementFields.NEW)
        _current_value = diff.get(ImportElementFields.CURRENT)
        if _new_value != _current_value:
            return True
    return _changed

def get_changed_elements(elements: list[dict]) -> dict[str, dict[str,Union[bool,str]]]:
    changed_elements = {}
    for element in elements:

        changed_fields = []
        for field, diff_field in element[ImportElementFields.DIFF].items():
            if not (diff_field[ImportElementFields.NEW] == diff_field[ImportElementFields.CURRENT]):
                changed_fields.append(field)
        if changed_fields:
            changed_elements[element['uri']] = {}
            changed_elements[element['uri']]['changed'] = bool(changed_fields)
            changed_elements[element['uri']]['changed_fields'] = changed_fields
    return changed_elements


def _test_helper_filter_updated_and_changed(elements: list[dict], updated_fields: Optional[tuple]) -> list[dict]:
    filter_func = partial(filter_changed_fields, updated_fields=updated_fields)
    changed_elements = filter(filter_func, elements)
    return list(changed_elements)


def _test_helper_change_fields_elements(elements,
                                        fields_to_update: Optional[tuple] = None,
                                        n=3) -> OrderedDict:
    """ elements test preparation function """

    if len(elements) < n:
        raise ValueError("Length of elements should not be smaller than n.")
    _new_elements = OrderedDict()
    for _n, (_uri, _element) in enumerate(elements.items()):
        if _n <= n - 1:
            initialize_import_element_dict(_element)
            for field in fields_to_update:
                original_value = _element[field] or ''
                new_val = UPDATE_FIELD_FUNCS[field](_n)
                track_changes_on_element(_element, field, new_val, original_value=original_value)
                _element[field] = new_val
        _new_elements[_uri] = _element
    return _new_elements


def parse_xml_and_import_elements(xml_file, shuffle_elements=False):
    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    if shuffle_elements:
        # Extract items from the OrderedDict
        items = list(elements.items())
        # Shuffle the list of items
        random.shuffle(items)
        elements = OrderedDict(items)
    imported_elements = import_elements(elements)
    return elements, root, imported_elements

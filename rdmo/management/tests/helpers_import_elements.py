from collections import OrderedDict
from functools import partial
from typing import Dict, List, Optional, Tuple, Union

from rdmo.core.imports import CURRENT_DATA_FIELD, ELEMENT_DIFF_FIELD_NAME, NEW_DATA_FIELD, track_changes_on_element
from rdmo.management.import_utils import initialize_import_element_dict

UPDATE_FIELD_FUNCS = {
    'comment': lambda text: f"this is a test comment {text}",
    'target_text': lambda text: f"test target_text {text}",
    'relation': lambda text: "notempty".format(),
}


def filter_changed_fields(element, updated_fields=None) -> bool:
    _changed = element.get('changed', False)
    if updated_fields is None:
        return _changed
    changes = element.get(ELEMENT_DIFF_FIELD_NAME, {})
    for field, diff in changes.items():
        if field not in updated_fields:
            continue
        _new_value = diff.get(NEW_DATA_FIELD)
        _current_value = diff.get(CURRENT_DATA_FIELD)
        if _new_value != _current_value:
            return True
    return _changed

def get_changed_elements(elements: List[Dict]) -> Dict[str, Dict[str,Union[bool,str]]]:
    changed_elements = {}
    for element in elements:

        changed_fields = []
        for key, diff_field in element[ELEMENT_DIFF_FIELD_NAME].items():
            if diff_field[NEW_DATA_FIELD] != diff_field[CURRENT_DATA_FIELD]:
                changed_fields += key
        if changed_fields:
            changed_elements[element['uri']] = {
                'changed': bool(changed_fields),
                'changed_fields': changed_fields,
            }
    return changed_elements


def _test_helper_filter_updated_and_changed(elements: List[Dict], updated_fields: Optional[Tuple]) -> List[Dict]:
    filter_func = partial(filter_changed_fields, updated_fields=updated_fields)
    changed_elements = filter(filter_func, elements)
    return list(changed_elements)


def _test_helper_change_fields_elements(elements,
                                        fields_to_update: Optional[Tuple] = None,
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

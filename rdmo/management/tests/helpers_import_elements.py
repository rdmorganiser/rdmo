from collections import OrderedDict
from functools import partial
from typing import Dict, List, Optional, Tuple

from rdmo.core.imports import track_changes_on_element
from rdmo.management.imports import _initialize_import_element_dict, set_element_diff_field_meta_info

UPDATE_FIELD_FUNCS = {
    'comment': lambda text: f"this is a test comment {text}",
    'target_text': lambda text: f"test target_text {text}",
    'relation': lambda text: "notempty".format(),
}


def filter_changed_fields(element, updated_fields=None) -> bool:
    if updated_fields is None:
        return element.get('changed', False)
    return element.get('changed', False) and any(i in updated_fields for i in element.get('changed_fields', []))


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
            _initialize_import_element_dict(_element)
            for field in fields_to_update:
                original_value = _element[field] or ''
                new_val = UPDATE_FIELD_FUNCS[field](_n)
                track_changes_on_element(_element, field, new_val, original_value=original_value)
                _element[field] = new_val
            set_element_diff_field_meta_info(_element)
        _new_elements[_uri] = _element
    return _new_elements

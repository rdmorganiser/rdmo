
from collections import OrderedDict
from typing import Dict, List, Tuple

from rdmo.core.xml import XmlParser

xml_error_files = [
    ('file-does-not-exist.xml', 'may not be blank'),
    ('xml/error.xml', 'syntax error'),
    ('xml/error-version.xml', 'RDMO XML Version: 99'),
    ('xml/elements/legacy/catalog-error-key.xml', 'Missing legacy elements'),
]

def read_xml_and_parse_to_elements(xml_file):

    xml_parser = XmlParser(file_name=xml_file)
    if xml_parser.errors:
        _msg = "\n".join(xml_parser.errors)
        raise ValueError(f"This test function should NOT raise any Exceptions. {_msg!s}")
    return xml_parser.parsed_elements, xml_parser.root

def _test_helper_change_fields_elements(elements, update_dict=None, n=3) -> Tuple[Dict, List]:
    """ xml test preparation function """

    update_dict = update_dict if update_dict is not None else {}
    _default_update_dict = {'comment':  "this is a test comment {}"}
    update_dict.update(**_default_update_dict)

    if len(elements) < n:
        raise ValueError("Length of elements should not be smaller than n.")
    _new_elements = OrderedDict()
    _changed_elements = OrderedDict()
    for _n,(_uri, _element) in enumerate(elements.items()):
        if _n <= n-1:
            updated_and_changed = {}
            changed_element = _element
            for k,val in update_dict.items():
                if isinstance(val, str):
                    val = val.format(_n)
                updated_and_changed[k]= {'current': _element[k], 'uploaded': val}
                _element[k] = val
            if updated_and_changed:
                changed_element['updated_and_changed'] = updated_and_changed
            _changed_elements[_uri] = changed_element
        _new_elements[_uri] = _element
    return _new_elements, list(_changed_elements.values())

def _test_helper_filter_updated_and_changed(elements: List[Dict]) -> List[Dict]:
    filtered_elements = filter(lambda x: x.get('updated_and_changed', False), elements)
    return list(filtered_elements)

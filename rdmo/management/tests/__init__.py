from rdmo.core.xml import convert_elements, flat_xml_to_elements, order_elements, read_xml_file


def read_xml_and_parse_to_elements(xml_file):
    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    parsed_elements = list(elements.values())
    return parsed_elements, root

def change_fields_elements(elements, update_dict=None, n=3):

    _default_update_dict = {'comment':  "this is a test comment {}"}

    if len(elements) < n:
        raise ValueError("Length of elements should not be smaller than n.")
    _new_elements = []
    _changed_elements = []
    for _n,_element in enumerate(elements):
        if _n <= n-1:
            _element['comment'] = _default_update_dict['comment'].format(_n)
            if update_dict is not None:
                _element.update (**update_dict)
            _changed_elements.append(_element)
        _new_elements.append(_element)
    return _new_elements, _changed_elements

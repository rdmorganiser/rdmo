import logging
import re

import defusedxml.ElementTree as ET

log = logging.getLogger(__name__)


def read_xml_file(file_name):
    try:
        return ET.parse(file_name).getroot()
    except Exception as e:
        log.error('Xml parsing error: ' + str(e))


def parse_xml_string(string):
    try:
        return ET.fromstring(string)
    except Exception as e:
        log.error('Xml parsing error: ' + str(e))


def flat_xml_to_elements(root):
    elements = {}
    ns_map = get_ns_map(root)
    uri_attrib = get_ns_tag('dc:uri', ns_map)

    for node in root:
        uri = get_uri(node, ns_map)

        element = {
            'type': node.tag,
            'uri': get_uri(node, ns_map)
        }

        for sub_node in node:
            tag = strip_ns(sub_node.tag, ns_map)

            if uri_attrib in sub_node.attrib:
                # this node has an uri!
                element[tag] = {
                    'uri': sub_node.attrib[uri_attrib]
                }
            elif 'lang' in sub_node.attrib:
                # this node has the lang attribute!
                element['%s_%s' % (tag, sub_node.attrib['lang'])] = sub_node.text
            elif list(sub_node):
                # this node is a list!
                element[tag] = []
                for sub_sub_node in sub_node:
                    sub_element = {
                        'uri': sub_sub_node.attrib[uri_attrib]
                    }
                    if 'order' in sub_sub_node.attrib:
                        sub_element['order'] = sub_sub_node.attrib['order']

                    element[tag].append(sub_element)
            elif sub_node.text is None or not sub_node.text.strip():
                element[tag] = None
            else:
                element[tag] = sub_node.text

        elements[uri] = element

    return elements


def get_ns_tag(tag, ns_map):
    tag_split = tag.split(':')
    try:
        return '{%s}%s' % (ns_map[tag_split[0]], tag_split[1])
    except KeyError:
        return None


def get_ns_map(treenode):
    ns_map = {}
    treestring = ET.tostring(treenode, encoding='utf8', method='xml')

    for match in re.finditer(r'(xmlns:)(.*?)(=")(.*?)(")', str(treestring)):
        if match:
            ns_map[match.group(2)] = match.group(4)

    return ns_map


def get_uri(treenode, ns_map):
    if treenode is not None:
        ns_tag = get_ns_tag('dc:uri', ns_map)
        if ns_tag is not None:
            return treenode.attrib.get(ns_tag)


def strip_ns(tag, ns_map):
    for ns in ns_map.values():
        if tag.startswith('{%s}' % ns):
            return tag.replace('{%s}' % ns, '')
    return tag


def filter_elements_by_type(elements, element_type):
    for element in elements:
        if element['type'] == element_type:
            yield element


def convert_elements(elements, version):
    # in future versions, this method can be extended
    # using packaging.version.parse
    if version is None:
        convert_legacy_elements(elements)


def convert_legacy_elements(elements):
    # first pass: identify pages
    for uri, element in elements.items():
        if element['type'] == 'questionset':
            if element.get('questionset') is None:
                # this is now a page
                element['type'] = 'page'
            else:
                del element['section']

    # second pass: del key, set uri_path, add order to reverse m2m through models
    # and sort questions into pages or questionsets
    for uri, element in elements.items():
        if element['type'] == 'catalog':
            element['uri_path'] = element.pop('key')

        elif element['type'] == 'section':
            del element['key']
            element['uri_path'] = element.pop('path')

            if element.get('catalog') is not None:
                element['catalog']['order'] = element.pop('order')

        elif element['type'] == 'page':
            del element['key']
            element['uri_path'] = element.pop('path')

            if element.get('section') is not None:
                element['section']['order'] = element.pop('order')

        elif element['type'] == 'questionset':
            del element['key']
            element['uri_path'] = element.pop('path')

            if element.get('questionset') is not None:
                element['questionset']['order'] = element.pop('order')

        elif element['type'] == 'question':
            del element['key']
            element['uri_path'] = element.pop('path')

            parent = element.get('questionset').get('uri')
            if parent is not None:
                if elements[parent].get('type') == 'page':
                    del element['questionset']
                    element['page'] = {
                        'uri': parent,
                        'order': element.pop('order')
                    }
                else:
                    element['questionset']['order'] = element.pop('order')

        elif element['type'] == 'optionset':
            element['uri_path'] = element.pop('key')

        elif element['type'] == 'option':
            del element['key']
            element['uri_path'] = element.pop('path')

            if element.get('optionset') is not None:
                element['optionset']['order'] = element.pop('order')


def order_elements(ordered_elements, unordered_elements, uri, element):
    if element is not None:
        for element_value in element.values():
            if isinstance(element_value, dict):
                sub_uri = element_value.get('uri')
                sub_element = unordered_elements.get(sub_uri)
                if sub_uri not in ordered_elements:
                    order_elements(ordered_elements, unordered_elements, sub_uri, sub_element)

            elif isinstance(element_value, list):
                for value in element_value:
                    sub_uri = value.get('uri')
                    sub_element = unordered_elements.get(sub_uri)
                    if sub_uri not in ordered_elements:
                        order_elements(ordered_elements, unordered_elements, sub_uri, sub_element)

        if uri not in ordered_elements:
            ordered_elements[uri] = element

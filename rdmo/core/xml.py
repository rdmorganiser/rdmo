import logging
import re

import defusedxml.ElementTree as ET

from .constants import IMPORT_SORT_ORDER


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


def flat_xml_to_elements(treenode):
    elements = []
    ns_map = get_ns_map(treenode)
    uri_attrib = get_ns_tag('dc:uri', ns_map)

    for node in treenode:

        element = {
            'uri': get_uri(node, ns_map),
            'type': node.tag
        }

        for subnode in node:
            tag = strip_ns(subnode.tag, ns_map)

            if uri_attrib in subnode.attrib:
                # this node has an uri!
                element[tag] = subnode.attrib[uri_attrib]
            elif 'lang' in subnode.attrib:
                # this node has the lang attribute!
                element['%s_%s' % (tag, subnode.attrib['lang'])] = subnode.text
            elif list(subnode):
                # this node is a list!
                element[tag] = [subsubnode.attrib[uri_attrib] for subsubnode in subnode]
            else:
                element[tag] = subnode.text

        elements.append(element)

    elements = sorted(elements, key=sort_elements)
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


def sort_elements(element):
    # remove the uri_prefix from the uri to create the key to be sorted by
    sort_key = element['uri'].replace(element['uri_prefix'], '')

    # remove the app name from the sort_key and replace it by its import order
    for i, item in enumerate(IMPORT_SORT_ORDER):
        if sort_key.startswith(item):
            sort_key = sort_key.replace(item, str(i))

    return sort_key

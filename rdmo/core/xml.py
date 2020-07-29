import logging
import re

import defusedxml.ElementTree as ET

log = logging.getLogger(__name__)


def read_xml_file(file_name):
    try:
        return ET.parse(file_name).getroot()
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

    elements = sort_elements_by_key(elements, 'uri')
    return elements


def get_ns_tag(tag, ns_map):
    tag_split = tag.split(':')
    return '{%s}%s' % (ns_map[tag_split[0]], tag_split[1])


def get_ns_map(treenode):
    ns_map = {}
    treestring = ET.tostring(treenode, encoding='utf8', method='xml')

    for match in re.finditer(r'(xmlns:)(.*?)(=")(.*?)(")', str(treestring)):
        if match:
            ns_map[match.group(2)] = match.group(4)

    return ns_map


def get_uri(treenode, ns_map):
    ns_tag = get_ns_tag('dc:uri', ns_map)
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


def sort_elements_by_key(dictlist, key, reverse=False):
    return sorted(dictlist, key=lambda k: k[key], reverse=reverse)

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


def flat_xml_to_elements(treenode, sort_parent_nodes=True):
    elements = []
    ns_map = get_ns_map(treenode)
    uri_attrib = get_ns_tag('dc:uri', ns_map)

    parent_nodes = get_parent_nodes(treenode)
    
    if sort_parent_nodes:
        parent_nodes = sort_elements_by_key(parent_nodes, 'uri')

    for node in parent_nodes:
        element = {
            'uri': node['uri'],
            'type': node['type'],
        }

        for subnode in node['node']:
            tag, value = get_tag_and_value_from_subnode(subnode, ns_map, uri_attrib)
            element[tag] = value

        elements.append(element)
        
    return elements

def get_parent_nodes(treenode):
    parent_nodes = []
    ns_map = get_ns_map(treenode)

    for node in treenode:

        node_element = {
            'uri': get_uri(node, ns_map),
            'type': node.tag,
            'node' : node
        }
        parent_nodes.append(node_element)

    return parent_nodes

    
def get_tag_and_value_from_subnode(subnode, ns_map, uri_attrib):

    # default tag
    tag = strip_ns(subnode.tag, ns_map)
    # default value
    value = subnode.text

    if uri_attrib in subnode.attrib:
        # this node has an uri!
        value = subnode.attrib[uri_attrib]
    elif 'lang' in subnode.attrib:
        # this node has the lang attribute!
        tag = '%s_%s' % (tag, subnode.attrib['lang'])
    elif list(subnode):
        # this node is a list!
        value =  [subsubnode.attrib[uri_attrib] for subsubnode in subnode]

    return tag, value


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

def sort_elements_by_key(dictlist, key, reverse=False):
    return sorted(dictlist, key=lambda k: k[key], reverse=reverse)
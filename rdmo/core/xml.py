import logging
import re
import defusedxml.ElementTree as ET

log = logging.getLogger(__name__)


def flat_xml_to_elements(treenode):
    elements = []
    ns_map = get_ns_map(treenode)
    uri_attrib = get_ns_tag('dc:uri', ns_map)

    for node in treenode:

        element = {
            'uri': get_uri(node, ns_map),
            'node_type': get_node_type(node)
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

    elements = sort_dictlist_by_key(elements, 'uri')
    return elements


def filter_elements_by_node_type(elements, node_type):
    for element in elements:
        if element['node_type'] == node_type:
            yield  element


def get_ns_tag(tag, nsmap):
    tag_split = tag.split(':')
    return '{%s}%s' % (nsmap[tag_split[0]], tag_split[1])


def get_ns_map(treenode):
    ns_map = {}
    treestring = ET.tostring(treenode, encoding='utf8', method='xml')
    match = re.search(r'(xmlns:)(.*?)(=")(.*?)(")', str(treestring))
    if bool(match) is True:
        ns_map = {match.group(2): match.group(4)}
    return ns_map


def get_uri(treenode, nsmap, method='text'):
    ns_tag = get_ns_tag('dc:uri', nsmap)
    uri = treenode.attrib[ns_tag]
    return str(uri)


def get_node_type(treenode):
    first_line = ET.tostring(treenode).split('\n')[0]
    node_type = re.search(r'(?<=<)[a-z]+', first_line).group(0)
    return node_type


def strip_ns(tag, ns_map):
    for ns in ns_map.values():
        if tag.startswith('{%s}' % ns):
            return tag.replace('{%s}' % ns, '')
    return tag


def sort_dictlist_by_key(dictlist, key, reverse=False):
    return sorted(dictlist, key=lambda k: k[key], reverse=reverse)

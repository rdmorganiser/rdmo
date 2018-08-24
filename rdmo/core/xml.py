import logging
import re
import defusedxml.ElementTree as ET

log = logging.getLogger(__name__)


def flat_xml_to_dictlist(treenode):
    dictlist = []
    nsmap = get_ns_map(treenode)
    for item in treenode:
        d = {}
        uri = get_uri(item, nsmap)
        node_type = get_node_type(item)

        for elem in item:
            tag = elem.tag
            if '}' in tag:
                tag = tag.split('}')[1]

            parent = None
            if 'parent' in str(elem):
                try:
                    parent = re.search(r'(?<=dc:uri=")[a-zA-Z0-9\.\/-_]+', ET.tostring(elem)).group(0)
                except AttributeError:
                    pass
            d[tag] = elem.text

        d['parent'] = parent
        d['uri'] = uri
        d['node_type'] = node_type
        d['uri_prefix'] = uri.split('/domain/')[0]
        dictlist.append(d)
    dictlist = sort_dictlist_by_key(dictlist, 'uri')
    return dictlist


def get_text_or_attribute(treenode, tagname, mode='text'):
    r = None
    el = treenode.find(tagname)
    try:
        if mode == 'text':
            r = el.text
        if mode == 'attribute':
            r = el.attrib
    except AttributeError:
        pass
    return r


def get_ns_tag(tag, nsmap):
    tag_split = tag.split(':')
    return '{%s}%s' % (nsmap[tag_split[0]], tag_split[1])


def get_ns_map(treenode):
    nsmap = {}
    treestring = ET.tostring(treenode, encoding='utf8', method='xml')
    match = re.search(r'(xmlns:)(.*?)(=")(.*?)(")', str(treestring))
    if bool(match) is True:
        nsmap = {match.group(2): match.group(4)}
    return nsmap


def get_uri(treenode, nsmap, method='text'):
    attrib = treenode.attrib
    nstag = get_ns_tag('dc:uri', nsmap)
    uri = attrib[nstag]
    return str(uri)


def get_node_type(treenode):
    first_line = ET.tostring(treenode).split('\n')[0]
    node_type = re.search(r'(?<=<)[a-z]+', first_line).group(0)
    return node_type


def node_type_from_dictlist(dictlist, node_type):
    newdictlist = []
    for el in dictlist:
        if el['node_type'] == node_type:
            newdictlist.append(el)
    return newdictlist


def sort_dictlist_by_key(dictlist, key, reverse=False):
    return sorted(dictlist, key=lambda k: k[key], reverse=reverse)

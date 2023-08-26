import logging
import re

import defusedxml.ElementTree as ET

log = logging.getLogger(__name__)

models = {
  'catalog': 'questions.catalog',
  'section': 'questions.section',
  'page': 'questions.page',
  'questionset': 'questions.questionset',
  'question': 'questions.question',
  'attribute': 'domain.attribute',
  'optionset': 'options.optionset',
  'option': 'options.option',
  'condition': 'conditions.condition',
  'task': 'tasks.task',
  'view': 'views.view'
}


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
            'uri': get_uri(node, ns_map),
            'model': models[node.tag]
        }

        for sub_node in node:
            tag = strip_ns(sub_node.tag, ns_map)

            if uri_attrib in sub_node.attrib:
                # this node has an uri!
                element[tag] = {
                    'uri': sub_node.attrib[uri_attrib]
                }
                if sub_node.tag in models:
                    element[tag]['model'] = models[sub_node.tag]
            elif 'lang' in sub_node.attrib:
                # this node has the lang attribute!
                element['{}_{}'.format(tag, sub_node.attrib['lang'])] = sub_node.text
            elif list(sub_node):
                # this node is a list!
                element[tag] = []
                for sub_sub_node in sub_node:
                    sub_element = {
                        'uri': sub_sub_node.attrib[uri_attrib]
                    }
                    if sub_sub_node.tag in models:
                        sub_element['model'] = models[sub_sub_node.tag]
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
        return f'{{{ns_map[tag_split[0]]}}}{tag_split[1]}'
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


def convert_elements(elements, version):
    # in future versions, this method can be extended
    # using packaging.version.parse
    if version is None:
        return convert_legacy_elements(elements)
    else:
        return elements


def convert_legacy_elements(elements):
    # first pass: identify pages
    for uri, element in elements.items():
        if element['model'] == 'questions.questionset':
            if element.get('questionset') is None:
                # this is now a page
                element['model'] = 'questions.page'
            else:
                del element['section']

    # second pass: del key, set uri_path, add order to reverse m2m through models
    # and sort questions into pages or questionsets
    for uri, element in elements.items():
        if element['model'] == 'conditions.condition':
            element['uri_path'] = element.pop('key')

        elif element['model'] == 'questions.catalog':
            element['uri_path'] = element.pop('key')

        elif element['model'] == 'questions.section':
            del element['key']
            element['uri_path'] = element.pop('path')

            if element.get('catalog') is not None:
                element['catalog']['order'] = element.pop('order')

        elif element['model'] == 'questions.page':
            del element['key']
            element['uri_path'] = element.pop('path')

            if element.get('section') is not None:
                element['section']['order'] = element.pop('order')

        elif element['model'] == 'questions.questionset':
            del element['key']
            element['uri_path'] = element.pop('path')

            parent = element.get('questionset').get('uri')
            if parent is not None:
                if elements[parent].get('model') == 'questions.page':
                    # this questionset belongs to a page now
                    del element['questionset']
                    element['page'] = {
                        'uri': parent,
                        'order': element.pop('order')
                    }
                else:
                    # this questionset still belongs to a questionset
                    element['questionset']['order'] = element.pop('order')

        elif element['model'] == 'questions.question':
            del element['key']
            element['uri_path'] = element.pop('path')

            parent = element.get('questionset').get('uri')
            if parent is not None:
                if elements[parent].get('model') == 'questions.page':
                    # this question belongs to a page now
                    del element['questionset']
                    element['page'] = {
                        'uri': parent,
                        'order': element.pop('order')
                    }
                else:
                    # this question still belongs to a questionset
                    element['questionset']['order'] = element.pop('order')

        elif element['model'] == 'options.optionset':
            element['uri_path'] = element.pop('key')

        elif element['model'] == 'options.option':
            del element['key']
            element['uri_path'] = element.pop('path')

            if element.get('optionset') is not None:
                element['optionset']['order'] = element.pop('order')

        if element['model'] == 'tasks.task':
            element['uri_path'] = element.pop('key')

        if element['model'] == 'views.view':
            element['uri_path'] = element.pop('key')

    return elements


def order_elements(elements):
    ordered_elements = {}
    for uri, element in elements.items():
        append_element(ordered_elements, elements, uri, element)
    return ordered_elements


def append_element(ordered_elements, unordered_elements, uri, element):
    if element is None:
        return

    for element_value in element.values():
        if isinstance(element_value, dict):
            sub_uri = element_value.get('uri')
            sub_element = unordered_elements.get(sub_uri)
            if sub_uri not in ordered_elements:
                append_element(ordered_elements, unordered_elements, sub_uri, sub_element)

        elif isinstance(element_value, list):
            for value in element_value:
                sub_uri = value.get('uri')
                sub_element = unordered_elements.get(sub_uri)
                if sub_uri not in ordered_elements:
                    append_element(ordered_elements, unordered_elements, sub_uri, sub_element)

    if uri not in ordered_elements:
        ordered_elements[uri] = element

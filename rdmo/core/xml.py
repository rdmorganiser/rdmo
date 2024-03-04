import logging
import re
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from django.utils.translation import gettext_lazy as _

import defusedxml.ElementTree as ET
from packaging.version import Version, parse

from rdmo import __version__ as VERSION

logger = logging.getLogger(__name__)

RDMO_MODELS = {
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

DEFAULT_RDMO_XML_VERSION = '1.11.0'
ELEMENTS_USING_KEY = {RDMO_MODELS['attribute']}


@dataclass
class XmlToElementsParser:

    file_name: str = None
    # post init attributes
    file: Path = None  # will be set from file_name
    root = None
    errors: list = field(default_factory=list)
    parsed_elements: OrderedDict = field(default_factory=OrderedDict)

    def __post_init__(self):
        if self.file_name is None:
            raise ValueError("File name is required.")
        self.file = Path(self.file_name).resolve()
        if not self.file.exists():
            raise ValueError(f"File does not exist. {self.file}")

        elements = self.parse_xml_to_elements(self.file)
        self.parsed_elements = elements
        self.errors.reverse()

    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.errors and raise_exception:  # raise for errors
            raise ValueError(self.errors)
        return not bool(self.errors)

    def parse_xml_to_elements(self, xml_file: Path, raise_exception:bool=False) -> Optional[OrderedDict]:
        root = None
        # step 2: parse xml
        try:
            root = read_xml_file(self.file, raise_exception=True)
        except Exception as e:
            self.errors.append(_('XML Parsing Error') + f': {e!s}')
            logger.info('XML parsing error. Import failed.')

        if root is None:
            self.errors.append(_('The content of the xml file does not consist of well formed data or markup.'))
            return
        elif root.tag != 'rdmo':
            self.errors.append(_('This XML does not contain RDMO content.'))
            return
        self.root = root

        # step 2.1: validate parsed xml
        unparsed_root_version = root.attrib.get('version') or DEFAULT_RDMO_XML_VERSION
        root_version, rdmo_version = parse(unparsed_root_version), parse(VERSION)
        if root_version > rdmo_version:
            logger.info(f'Import failed version validation ({root_version} > {rdmo_version})')
            self.errors.append(_('This RDMO XML file does not have a valid version number.'))
            self.errors.append(f'RDMO XML Version: {root_version}')
            return

        # step 3: create element dicts from xml
        elements = OrderedDict()
        try:
            elements = flat_xml_to_elements(root)
        except KeyError as e:
            logger.info('Import failed with KeyError (%s)' % e)
            self.errors.append(_('This is not a valid RDMO XML file.'))
        except TypeError as e:
            logger.info('Import failed with TypeError (%s)' % e)
            self.errors.append(_('This is not a valid RDMO XML file.'))
        except AttributeError as e:
            logger.info('Import failed with AttributeError (%s)' % e)
            self.errors.append(_('This is not a valid RDMO XML file.'))
        if self.errors:
            return

        # step 3.1: validate elements for legacy versions
        try:
            pre_conversion_validate_missing_key_in_legacy_elements(elements, root_version)
        except ValueError as e:
            logger.info('Import failed with ValueError (%s)' % e)
            self.errors.append(_('XML Parsing Error') + f': {e!s}')
            self.errors.append(_('This is not a valid RDMO XML file.'))
        if self.errors:
            return
        # step 4: convert elements from previous versions
        elements = convert_elements(elements, root_version)

        # step 5: order the elements and return
        elements = order_elements(elements)

        logger.info(f'XML parsing of {self.file.name} success (length: {len(elements)}).')
        return elements


def read_xml_file(file_name, raise_exception=False):
    try:
        return ET.parse(file_name).getroot()
    except Exception as e:
        logger.error('Xml parsing error: ' + str(e))
        if raise_exception:
            raise e from e


def parse_xml_string(string):
    try:
        return ET.fromstring(string)
    except Exception as e:
        logger.error('Xml parsing error: ' + str(e))


def flat_xml_to_elements(root):
    elements = {}
    ns_map = get_ns_map(root)
    uri_attrib = get_ns_tag('dc:uri', ns_map)

    for node in root:
        uri = get_uri(node, ns_map)

        element = {
            'uri': get_uri(node, ns_map),
            'model': RDMO_MODELS[node.tag]
        }

        for sub_node in node:
            tag = strip_ns(sub_node.tag, ns_map)

            if uri_attrib in sub_node.attrib:
                # this node has an uri!
                element[tag] = {
                    'uri': sub_node.attrib[uri_attrib]
                }
                if sub_node.tag in RDMO_MODELS:
                    element[tag]['model'] = RDMO_MODELS[sub_node.tag]
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
                    if sub_sub_node.tag in RDMO_MODELS:
                        sub_element['model'] = RDMO_MODELS[sub_sub_node.tag]
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


def convert_elements(elements, version: Version):
    if not isinstance(version, Version):
        raise TypeError('Version should be a parsed version type. (parse(version))')
    if version < parse('2.0.0'):
        pre_conversion_validate_missing_key_in_legacy_elements(elements, version)
        elements = convert_legacy_elements(elements)

    if version < parse('2.1.0'):
        elements = convert_additional_input(elements)

    return elements


def pre_conversion_validate_missing_key_in_legacy_elements(elements, version: Version) -> None:
    if version < parse('2.0.0'):
        models_in_elements = {i['model'] for i in elements.values()}
        if models_in_elements <= ELEMENTS_USING_KEY:
            # xml contains only domain.attribute or is empty
            return
        # inspect the elements for missing 'key' fields
        elements_to_inspect = filter(lambda x: x['model'] not in ELEMENTS_USING_KEY, elements.values())
        inspected_elements_containing_key = list(filter(lambda x: 'key' in x, elements_to_inspect))
        if not inspected_elements_containing_key:
            raise ValueError(f"Missing legacy elements, elements containing 'key' were expected for this XML with version {version} and elements {models_in_elements}.")   # noqa: E501


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


def convert_additional_input(elements):
    for uri, element in elements.items():
        if element['model'] == 'options.option':
            additional_input = element.get('additional_input')
            if additional_input == 'True':
                element['additional_input'] = 'text'
            else:
                element['additional_input'] = ''

    return elements


def order_elements(elements):
    ordered_elements = OrderedDict()
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

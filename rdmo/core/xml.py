import logging
import re
from collections import OrderedDict
from pathlib import Path
from typing import Dict, Optional, Tuple
from xml.etree.ElementTree import Element as xmlElement

from django.utils.translation import gettext_lazy as _

import defusedxml.ElementTree as ET
from packaging.version import Version, parse

from rdmo import __version__ as RDMO_INSTANCE_VERSION
from rdmo.core.constants import RDMO_MODELS
from rdmo.core.imports import ImportElementFields

logger = logging.getLogger(__name__)

LEGACY_RDMO_XML_VERSION = '1.11.0'
ELEMENTS_USING_KEY = {RDMO_MODELS['attribute']}


def resolve_file(file_name: str) -> Tuple[Optional[Path], Optional[str]]:
    file = Path(file_name).resolve()
    if file.exists():
        return file, None
    return  None, _('This file does not exists.')


def read_xml(file: Path) -> Tuple[Optional[xmlElement], Optional[str]]:
    # step 2: parse xml and get the root
    try:
        root = ET.parse(file).getroot()
        return root, None
    except Exception as e:
        return None, _('XML Parsing Error') + f': {e!s}'


def validate_root(root: Optional[xmlElement]) -> Tuple[bool, Optional[str]]:
    if root is None:
        return False, _('The content of the XML file does not consist of well-formed data or markup.')
    if root.tag != 'rdmo':
        return False, _('This XML does not contain RDMO content.')
    return True, None


def validate_and_get_xml_version_from_root(root: xmlElement) -> Tuple[Optional[Version], list]:
    unparsed_root_version = root.attrib.get('version') or LEGACY_RDMO_XML_VERSION
    root_version, rdmo_version = parse(unparsed_root_version), parse(RDMO_INSTANCE_VERSION)
    if root_version > rdmo_version:
        logger.info('Import failed version validation (%s > %s)', root_version, rdmo_version)
        errors = [
            _('This RDMO XML file does not have a valid version number.'),
            f'XML Version ({root_version}) is greater than RDMO instance version {rdmo_version}'
        ]
        return None, errors
    return root_version, []


def validate_legacy_elements(elements: dict, root_version: Version) -> list:

    try:
        validate_pre_conversion_for_missing_key_in_legacy_elements(elements, root_version)
        return []
    except ValueError as e:
        logger.info('Import failed with ValueError (%s)', str(e))
        errors = [
            _('XML Parsing Error') + f': {e!s}',
            _('This is not a valid RDMO XML file.')
        ]
        return errors


def parse_elements(root: xmlElement) -> Tuple[Dict, Optional[str]]:
    # step 3: create element dicts from xml
    try:
        elements = flat_xml_to_elements(root)
        return elements, None
    except (KeyError, TypeError, AttributeError) as e:
        logger.info('Import failed with %s (%s)', type(e).__name__, e)
        return {}, _('This is not a valid RDMO XML file.')


def parse_xml_to_elements(xml_file=None) -> Tuple[OrderedDict, list]:

    errors = []

    file, file_error = resolve_file(xml_file)
    if file_error is not None:
        logger.error(file_error)
        errors.append(file_error)
        return OrderedDict(), errors

    root, read_error = read_xml(file)

    if read_error:
        logger.error(read_error)
        errors.append(read_error)

    # step 2.1: validate the xml root
    root_validation, root_validation_error = validate_root(root)
    if root_validation is not True:
        logger.error('Root element validation failed. %s', root_validation_error)
        errors.insert(0, root_validation_error)
        return OrderedDict(), errors

    # step 3: create element dicts from xml
    elements, parsing_error = parse_elements(root)
    if parsing_error is not None:
        errors.append(parsing_error)
        return OrderedDict(), errors

    # step 3.1: validate version
    root_version, version_errors = validate_and_get_xml_version_from_root(root)
    if version_errors:
        errors.extend(version_errors)
        return OrderedDict(), errors

    # step 3.1.1: validate the legacy elements
    legacy_errors = validate_legacy_elements(elements, parse(root.attrib.get('version', LEGACY_RDMO_XML_VERSION)))
    if legacy_errors:
        errors.extend(legacy_errors)
        return OrderedDict(), errors

    # step 4: convert elements from previous versions
    elements = convert_elements(elements, parse(root.attrib.get('version', LEGACY_RDMO_XML_VERSION)))

    # step 5: order the elements and return
    # ordering of elements is done in the import_elements function

    logger.info('XML parsing of %s success (length: %s).', file.name, len(elements))

    return elements, errors


def read_xml_file(file_name, raise_exception=False):
    try:
        return ET.parse(file_name).getroot()
    except Exception as e:
        logger.error('Xml file parsing error at getroot: %s', str(e))
        if raise_exception:
            raise e from e


def parse_xml_string(string):
    try:
        return ET.fromstring(string)
    except Exception as e:
        logger.error('Xml parsing from string error: %s', str(e))


def flat_xml_to_elements(root) -> dict:
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
        if tag.startswith(f'{{{ns}}}'):
            return tag.replace(f'{{{ns}}}', '')
    return tag


def convert_elements(elements, version: Version):
    if not isinstance(version, Version):
        raise TypeError('Version should be of parsed version type.')

    if version < parse('2.0.0'):
        validate_pre_conversion_for_missing_key_in_legacy_elements(elements, version)
        elements = convert_legacy_elements(elements)

    if version < parse('2.1.0'):
        elements = convert_additional_input(elements)

    return elements


def validate_pre_conversion_for_missing_key_in_legacy_elements(elements, version: Version) -> None:
    if version < parse('2.0.0'):
        models_in_elements = {i['model'] for i in elements.values()}
        if models_in_elements <= ELEMENTS_USING_KEY:
            # xml contains only domain.attribute or is empty
            return
        # inspect the elements for missing 'key' fields
        elements_to_inspect = filter(lambda x: x['model'] not in ELEMENTS_USING_KEY, elements.values())
        if not any('key' in el for el in elements_to_inspect):
            raise ValueError(f"Missing legacy elements, elements containing 'key' were expected for this XML with version {version} and elements {models_in_elements}.")   # noqa: E501


def update_related_legacy_elements(elements: Dict,
                                   target_uri: str, source_model: str,
                                   legacy_element_field: str, element_field: str):
    # search for the related elements that use the uri
    related_elements = [
        element for element in elements.values()
        if element['model'] == source_model
        and element.get(legacy_element_field, {}).get('uri') == target_uri
    ]
    # write the related elements back into the related element
    elements[target_uri][element_field] = [
        {k: v for k, v in element.items() if k in ('uri', 'model', 'order')}
        for element in related_elements
    ]


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
            # Add sections to the catalog
            update_related_legacy_elements(elements, uri, 'questions.section', 'catalog', 'sections')

        elif element['model'] == 'questions.section':
            del element['key']
            element['uri_path'] = element.pop('path')
            del element['catalog']  # sections do not have catalog anymore
            # Add section_pages to the section
            update_related_legacy_elements(elements, uri, 'questions.page', 'section', 'pages')

        elif element['model'] == 'questions.page':
            del element['key']
            element['uri_path'] = element.pop('path')
            del element['section']  # pages do not have sections anymore

            # Add page_questionsets to the page
            # Add questionsets to the page
            update_related_legacy_elements(elements, uri, 'questions.questionset', 'questionset', 'questionsets')

            # Add page_questions to the page
            update_related_legacy_elements(elements, uri, 'questions.question', 'question', 'questions')

            # Add page_conditions to the page
            update_related_legacy_elements(elements, uri, 'conditions.condition', 'condition', 'conditions')

        elif element['model'] == 'questions.questionset':
            del element['key']
            element['uri_path'] = element.pop('path')

            parent = element.get('questionset').get('uri')
            if parent is not None:
                if elements[parent].get('model') == 'questions.page':
                    # this questionset belongs to a page now
                    parent_questionsets = elements[parent].get('questionset')
                    parent_questionsets = parent_questionsets or []
                    parent_questionsets.append({
                        'uri': element['uri'],
                        'model': element['model'],
                        'order': element.pop('order')
                    })
                    elements[parent]['questionset'] = parent_questionsets
                    del element['questionset']
                else:
                    # this questionset still belongs to a questionset
                    element['questionset']['order'] = element.pop('order')

        elif element['model'] == 'questions.question':
            del element['key']
            element['uri_path'] = element.pop('path')

            parent = element.get('questionset').get('uri')
            if parent is not None:
                parent_questionsets = elements[parent].get('questions', [])
                parent_questionsets.append({
                    'uri': element['uri'],
                    'model': element['model'],
                    'order': element.pop('order')
                })
                elements[parent]['questions'] = parent_questionsets
                del element['questionset']

        elif element['model'] == 'options.optionset':
            element['uri_path'] = element.pop('key')

            update_related_legacy_elements(elements, uri, 'options.option', 'optionset', 'options')

        elif element['model'] == 'options.option':
            del element['key']
            element['uri_path'] = element.pop('path')

            del element['optionset']  # options do not have optionsets anymore


        if element['model'] == 'tasks.task':
            element['uri_path'] = element.pop('key')

        if element['model'] == 'views.view':
            element['uri_path'] = element.pop('key')

    return elements


def convert_additional_input(elements):
    for uri, element in elements.items():
        if element['model'] == 'options.option':
            additional_input = element.get('additional_input')
            if additional_input in ['', 'text', 'textarea']:  # from Option.ADDITIONAL_INPUT_CHOICES
                pass
            elif additional_input == 'True':
                element['additional_input'] = 'text'
            else:
                element['additional_input'] = ''

    return elements


def order_elements(elements: OrderedDict) -> OrderedDict:
    ordered_elements = OrderedDict()
    for uri, element in reversed(elements.items()):
        append_element(ordered_elements, elements, uri, element,)
    return ordered_elements


def append_element(ordered_elements, unordered_elements, uri, element) -> None:
    if element is None:
        return
    for key, element_value in element.items():
        if key in list(ImportElementFields):
            continue

        if isinstance(element_value, dict):
            sub_uri = element_value.get('uri')
            sub_element = unordered_elements.get(sub_uri)
            if sub_uri not in ordered_elements and sub_uri is not None:
                append_element(ordered_elements, unordered_elements, sub_uri, sub_element)

        elif isinstance(element_value, list):
            for value in element_value:
                sub_uri = value.get('uri')
                sub_element = unordered_elements.get(sub_uri)
                if sub_uri not in ordered_elements and sub_uri is not None:
                    append_element(ordered_elements, unordered_elements, sub_uri, sub_element)

    if uri not in ordered_elements:
        ordered_elements[uri] = element

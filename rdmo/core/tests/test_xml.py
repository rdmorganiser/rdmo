# import os
# import xml.etree.ElementTree as ET

# from ..imports import read_xml_file
# from ..xml import (flat_xml_to_dictlist, get_ns_map, get_ns_tag,
#                    get_text_or_attribute, get_uri, node_type_from_dictlist,
#                    sort_dictlist_by_key)


# # tests
# def test_get_ns_map():
#     xmls = read_all_test_xmls()
#     for key in xmls:
#         assert str(get_ns_map(xmls[key])) == "{'dc': 'http://purl.org/dc/elements/1.1/'}"


# def test_get_ns_tag():
#     root = read_test_xml('domain')
#     nsmap = get_ns_map(root)
#     assert get_ns_tag('dc:uri', nsmap) == "{http://purl.org/dc/elements/1.1/}uri"


# def test_get_text_or_attribute():
#     root = read_test_xml('domain')
#     el = root.find('attribute')
#     assert get_text_or_attribute(el, 'key') == 'set'
#     assert get_text_or_attribute(el, 'does_not_exist') is None


# def test_get_uri():
#     root = read_test_xml('domain')
#     el = root.find('attribute')
#     nsmap = get_ns_map(root)
#     assert get_uri(el, nsmap) == 'http://example.com/terms/domain/set'


# def test_etree_to_dict():
#     root = read_test_xml('domain')
#     dictlist = flat_xml_to_dictlist(root)
#     assert dictlist[0]['uri'] == 'http://example.com/terms/domain/conditions'
#     assert dictlist[1]['parent'] == 'http://example.com/terms/domain/conditions'

#     root = read_test_xml('conditions')
#     dictlist = flat_xml_to_dictlist(root)
#     assert dictlist[0]['uri'] == 'http://example.com/terms/conditions/options_empty'

#     root = read_test_xml('options')
#     dictlist = flat_xml_to_dictlist(root)
#     assert dictlist[0]['uri'] == 'http://example.com/terms/options/one_two_three'

#     root = read_test_xml('tasks')
#     dictlist = flat_xml_to_dictlist(root)
#     assert dictlist[0]['uri'] == 'http://example.com/terms/tasks/options_contains_one'

#     root = read_test_xml('questions')
#     dictlist = flat_xml_to_dictlist(root)
#     assert dictlist[0]['uri'] == 'http://example.com/terms/questions/catalog'

#     root = read_test_xml('views')
#     dictlist = flat_xml_to_dictlist(root)
#     assert dictlist[0]['uri'] == 'http://example.com/terms/views/view_a'


# def test_node_type_from_dictlist():
#     root = read_test_xml('options')
#     dictlist = flat_xml_to_dictlist(root)
#     optionsets = node_type_from_dictlist(dictlist, 'optionset')
#     assert optionsets[0]['node_type'] == 'optionset'


# # test utils
# def read_all_test_xmls():
#     xml = {}
#     xml['domain'] = read_test_xml('domain')
#     xml['conditions'] = read_test_xml('conditions')
#     xml['options'] = read_test_xml('options')
#     xml['project'] = read_test_xml('project')
#     xml['questions'] = read_test_xml('questions')
#     xml['tasks'] = read_test_xml('tasks')
#     xml['views'] = read_test_xml('views')
#     return xml


# def read_test_xml(filename):
#     xml_folder = os.getcwd().split('rdmo')[0] + 'rdmo/testing/xml/'
#     return read_xml_file(xml_folder + filename + '.xml')

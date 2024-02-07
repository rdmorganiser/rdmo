from pathlib import Path

from ..xml import flat_xml_to_elements, get_ns_map, get_ns_tag, get_uri, read_xml_file


def test_get_ns_map(settings):
    xml_path = Path(settings.BASE_DIR) / 'xml/elements/attributes.xml'
    root = read_xml_file(xml_path)
    assert get_ns_map(root) == {'dc': 'http://purl.org/dc/elements/1.1/'}


def test_get_ns_tag(settings):
    xml_path = Path(settings.BASE_DIR) / 'xml/elements/attributes.xml'
    root = read_xml_file(xml_path)
    nsmap = get_ns_map(root)
    assert get_ns_tag('dc:uri', nsmap) == "{http://purl.org/dc/elements/1.1/}uri"


def test_get_uri(settings):
    xml_path = Path(settings.BASE_DIR) / 'xml/elements/attributes.xml'
    root = read_xml_file(xml_path)
    el = root.find('attribute')
    nsmap = get_ns_map(root)
    assert get_uri(el, nsmap) == 'http://example.com/terms/domain/blocks'


def test_flat_xml_to_elements(settings):
    xml_path = Path(settings.BASE_DIR) / 'xml/elements/attributes.xml'
    root = read_xml_file(xml_path)
    elements = flat_xml_to_elements(root)
    assert elements['http://example.com/terms/domain/blocks']['uri'] == 'http://example.com/terms/domain/blocks'

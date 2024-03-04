
from rdmo.core.xml import XmlToElementsParser

xml_error_files = [
    ('file-does-not-exist.xml', 'may not be blank'),
    ('xml/error.xml', 'syntax error'),
    ('xml/error-version.xml', 'RDMO XML Version: 99'),
    ('xml/elements/legacy/catalog-error-key.xml', 'Missing legacy elements'),
]


def read_xml_and_parse_to_elements(xml_file):

    xml_parser = XmlToElementsParser(file_name=xml_file)
    if xml_parser.errors:
        _msg = "\n".join(map(str, xml_parser.errors))
        raise ValueError(f"This test function should NOT raise any Exceptions. {_msg!s}")
    return xml_parser.parsed_elements, xml_parser.root

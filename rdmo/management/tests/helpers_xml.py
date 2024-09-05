
from rdmo.core.xml import parse_xml_to_elements, read_xml, resolve_file

xml_test_files = {
    "xml/elements/catalogs.xml":
        None,
    "xml/elements/updated-and-changed/optionsets-1.xml":
        None,
    'file-does-not-exist.xml':
        'This file does not exists',
    "xml/error.xml":
        "The content of the XML file does not consist of well-formed data or markup. XML Parsing Error: syntax error: line 1, column 0",  # noqa: E501
    "xml/project.xml":
        "This XML does not contain RDMO content.",
    'xml/error-version.xml':
        'This RDMO XML file does not have a valid version number. XML Version (99.9.9) is greater',
    'xml/elements/legacy/catalog-error-key.xml':
        'XML Parsing Error: Missing legacy elements',
}

xml_error_files = {k: v for k,v in xml_test_files.items() if v is not None}
xml_error_files['file-does-not-exist.xml'] = 'This field may not be blank.'

def read_xml_and_parse_to_root_and_elements(file):
    errors = []

    xml_file, file_error = resolve_file(file)
    if file_error:
        errors.append(file_error)

    root, read_error = read_xml(xml_file)
    if read_error:
        errors.append(read_error)

    xml_parsed_elements, xml_parsing_errors = parse_xml_to_elements(xml_file=xml_file)
    if xml_parsing_errors:
        errors.extend(xml_parsing_errors)

    if errors:
        _msg = "\n".join(map(str, xml_parsing_errors))
        raise ValueError(f"This test function should NOT raise any Exceptions. {_msg!s}")
    return xml_parsed_elements, root

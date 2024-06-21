from pathlib import Path

from rdmo.core.xml import convert_elements, flat_xml_to_elements, order_elements, read_xml_file
from rdmo.management.imports import import_elements
from rdmo.questions.models import Catalog, Page, Question, QuestionSet, Section


def test_create_catalogs(db, settings):
    Catalog.objects.all().delete()
    Section.objects.all().delete()
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'catalogs.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == len(elements) == 148
    assert Catalog.objects.count() == 2
    assert Section.objects.count() == 6
    assert Page.objects.count() == 48
    assert QuestionSet.objects.count() == 3
    assert Question.objects.count() == 89
    assert all(element['created'] is True for element in elements)
    assert all(element['updated'] is False for element in elements)


def test_update_catalogs(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'catalogs.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == len(elements) == 148
    assert all(element['created'] is False for element in elements)
    assert all(element['updated'] is True for element in elements)


def test_create_sections(db, settings):
    Section.objects.all().delete()
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'sections.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == len(elements) == 146
    assert Section.objects.count() == 6
    assert Page.objects.count() == 48
    assert QuestionSet.objects.count() == 3
    assert Question.objects.count() == 89
    assert all(element['created'] is True for element in elements)
    assert all(element['updated'] is False for element in elements)


def test_update_sections(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'sections.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == len(elements) == 146
    assert all(element['created'] is False for element in elements)
    assert all(element['updated'] is True for element in elements)


def test_create_pages(db, settings):
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'pages.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == len(elements) == 140
    assert Page.objects.count() == 48
    assert QuestionSet.objects.count() == 3
    assert Question.objects.count() == 89
    assert all(element['created'] is True for element in elements)
    assert all(element['updated'] is False for element in elements)


def test_update_pages(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'pages.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == len(elements) == 140
    assert all(element['created'] is False for element in elements)
    assert all(element['updated'] is True for element in elements)


def test_create_questionsets(db, settings):
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questionsets.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == 10  # two questionsets appear twice in the export file
    assert len(elements) == 8
    assert QuestionSet.objects.count() == 3
    assert Question.objects.count() == 5
    assert all(element['created'] is True for element in elements)
    assert all(element['updated'] is False for element in elements)


def test_update_questionsets(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questionsets.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == 10  # two questionsets appear twice in the export file
    assert all(element['created'] is False for element in elements)
    assert all(element['updated'] is True for element in elements)


def test_create_questions(db, settings):
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questions.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == len(elements) == 89
    assert Question.objects.count() == 89
    assert all(element['created'] is True for element in elements)
    assert all(element['updated'] is False for element in elements)


def test_update_questions(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questions.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == len(elements) == 89
    assert all(element['created'] is False for element in elements)
    assert all(element['updated'] is True for element in elements)


def test_create_legacy_questions(db, settings):
    Catalog.objects.all().delete()
    Section.objects.all().delete()
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'questions.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == len(elements) == 147
    assert Catalog.objects.count() == 1
    assert Section.objects.count() == 6
    assert Page.objects.count() == 48
    assert QuestionSet.objects.count() == 3
    assert Question.objects.count() == 89
    assert all(element['created'] is True for element in elements)
    assert all(element['updated'] is False for element in elements)

    # check that all elements ended up in the catalog
    catalog = Catalog.objects.prefetch_elements().first()
    descendant_uris = {element.uri for element in catalog.descendants}
    element_uris = {element['uri'] for element in elements if element['uri'] != catalog.uri}
    assert descendant_uris == element_uris


def test_update_legacy_questions(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'questions.xml'

    root = read_xml_file(xml_file)
    version = root.attrib.get('version')
    elements = flat_xml_to_elements(root)
    elements = convert_elements(elements, version)
    elements = order_elements(elements)
    elements = elements.values()
    import_elements(elements)

    assert len(root) == len(elements) == 147
    assert all(element['created'] is False for element in elements)
    assert all(element['updated'] is True for element in elements)

    # check that all elements ended up in the catalog
    catalog = Catalog.objects.prefetch_elements().first()
    descendant_uris = {
        element.uri for element in catalog.descendants if any(element.uri.startswith(uri) for uri in [
            'http://example.com/terms/questions/catalog/individual',
            'http://example.com/terms/questions/catalog/set',
            'http://example.com/terms/questions/catalog/collections',
            'http://example.com/terms/questions/catalog/conditions',
            'http://example.com/terms/questions/catalog/options',
            'http://example.com/terms/questions/catalog/blocks'
        ])
    }
    element_uris = {element['uri'] for element in elements if element['uri'] != catalog.uri}
    assert descendant_uris == element_uris

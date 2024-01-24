from pathlib import Path

import pytest

from rdmo.management.imports import import_elements
from rdmo.questions.models import Catalog, Page, Question, QuestionSet, Section

from . import change_fields_elements, read_xml_and_parse_to_elements

imported_update_changes = [None]


def test_create_catalogs(db, settings):
    Catalog.objects.all().delete()
    Section.objects.all().delete()
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'catalogs.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 148
    assert Catalog.objects.count() == 2
    assert Section.objects.count() == 6
    assert Page.objects.count() == 48
    assert QuestionSet.objects.count() == 3
    assert Question.objects.count() == 89
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_catalogs(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'catalogs.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 148
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


@pytest.mark.parametrize('update_dict', imported_update_changes)
def test_update_catalogs_with_changed_fields(db, settings, update_dict):
    Catalog.objects.all().delete()
    Section.objects.all().delete()
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'catalogs.xml'
    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)
    assert len(root) == len(imported_elements) == 148
    # start test with fresh elements in db

    elements, changed_elements = change_fields_elements(elements, update_dict=update_dict, n=75)
    imported_elements = import_elements(elements)
    imported_and_changed = [i for i in elements if i['updated_and_changed']]
    assert len(imported_elements) == 148
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
        assert test['updated_and_changed'] == imported['updated_and_changed']


def test_create_sections(db, settings):
    Section.objects.all().delete()
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'sections.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 146
    assert Section.objects.count() == 6
    assert Page.objects.count() == 48
    assert QuestionSet.objects.count() == 3
    assert Question.objects.count() == 89
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_sections(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'sections.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 146
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


@pytest.mark.parametrize('update_dict', imported_update_changes)
def test_update_sections_with_changed_fields(db, settings, update_dict):
    Catalog.objects.all().delete()
    Section.objects.all().delete()
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'sections.xml'
    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)
    assert len(root) == len(imported_elements) == 146
    # start test with fresh elements in db

    elements, changed_elements = change_fields_elements(elements, update_dict=update_dict, n=75)
    imported_elements = import_elements(elements)
    imported_and_changed = [i for i in elements if i['updated_and_changed']]
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
        assert test['updated_and_changed'] == imported['updated_and_changed']


def test_create_pages(db, settings):
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'pages.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 140
    assert Page.objects.count() == 48
    assert QuestionSet.objects.count() == 3
    assert Question.objects.count() == 89
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_pages(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'pages.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 140
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


@pytest.mark.parametrize('update_dict', imported_update_changes)
def test_update_pages_with_changed_fields(db, settings, update_dict):
    Catalog.objects.all().delete()
    Section.objects.all().delete()
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'pages.xml'
    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)
    assert len(root) == len(imported_elements) == 140
    # start test with fresh elements in db
    elements, changed_elements = change_fields_elements(elements, update_dict=update_dict, n=75)
    imported_elements = import_elements(elements)
    imported_and_changed = [i for i in elements if i['updated_and_changed']]
    assert len(imported_elements) == 140
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
        assert test['updated_and_changed'] == imported['updated_and_changed']


def test_create_questionsets(db, settings):
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questionsets.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == 10  # two questionsets appear twice in the export file
    assert len(imported_elements) == 8
    assert QuestionSet.objects.count() == 3
    assert Question.objects.count() == 5
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_questionsets(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questionsets.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == 10  # two questionsets appear twice in the export file
    assert len(imported_elements) == 8
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


@pytest.mark.parametrize('update_dict', imported_update_changes)
def test_update_questionsets_with_changed_fields(db, settings, update_dict):
    Catalog.objects.all().delete()
    Section.objects.all().delete()
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questionsets.xml'
    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)
    assert len(root) == 10  # two questionsets appear twice in the export file
    assert len(imported_elements) == 8
    # start test with fresh elements in db
    elements, changed_elements = change_fields_elements(elements, update_dict=update_dict, n=5)
    imported_elements = import_elements(elements)
    imported_and_changed = [i for i in elements if i['updated_and_changed']]
    assert len(imported_elements) == 8
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
        assert test['updated_and_changed'] == imported['updated_and_changed']


def test_create_questions(db, settings):
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questions.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 89
    assert Question.objects.count() == 89
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_questions(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questions.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 89
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


@pytest.mark.parametrize('update_dict', imported_update_changes)
def test_update_questions_with_changed_fields(db, settings, update_dict):
    Catalog.objects.all().delete()
    Section.objects.all().delete()
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questions.xml'
    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)
    assert len(root) == len(imported_elements) == 89
    # start test with fresh elements in db
    elements, changed_elements = change_fields_elements(elements, update_dict=update_dict, n=45)
    imported_elements = import_elements(elements)
    imported_and_changed = [i for i in elements if i['updated_and_changed']]
    assert len(imported_elements) == 89
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
        assert test['updated_and_changed'] == imported['updated_and_changed']


def test_create_legacy_questions(db, settings):
    Catalog.objects.all().delete()
    Section.objects.all().delete()
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'questions.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 147
    assert Catalog.objects.count() == 1
    assert Section.objects.count() == 6
    assert Page.objects.count() == 48
    assert QuestionSet.objects.count() == 3
    assert Question.objects.count() == 89
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)

    # check that all elements ended up in the catalog
    catalog = Catalog.objects.prefetch_elements().first()
    descendant_uris = {element.uri for element in catalog.descendants}
    element_uris = {element['uri'] for element in elements if element['uri'] != catalog.uri}
    assert descendant_uris == element_uris


def test_update_legacy_questions(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'questions.xml'

    elements, root = read_xml_and_parse_to_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 147
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)

    # check that all elements ended up in the catalog
    catalog = Catalog.objects.prefetch_elements().first()
    descendant_uris = {element.uri for element in catalog.descendants}
    element_uris = {element['uri'] for element in elements if element['uri'] != catalog.uri}
    assert descendant_uris == element_uris

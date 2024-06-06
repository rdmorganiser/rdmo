from pathlib import Path

import pytest

from rdmo.core.imports import ELEMENT_DIFF_FIELD_NAME
from rdmo.management.imports import import_elements
from rdmo.questions.models import Catalog, Page, Question, QuestionSet, Section

from .helpers_import_elements import (
    _test_helper_change_fields_elements,
    _test_helper_filter_updated_and_changed,
)
from .helpers_models import delete_all_objects
from .helpers_xml import read_xml_and_parse_to_root_and_elements

fields_to_be_changed = (('comment',),)


def test_create_catalogs(db, settings):
    delete_all_objects([Catalog, Section, Page, QuestionSet, Question])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'catalogs.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
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

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 148
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


@pytest.mark.parametrize('updated_fields', fields_to_be_changed)
def test_update_catalogs_with_changed_fields(db, settings, updated_fields):
    delete_all_objects([Catalog, Section, Page, QuestionSet, Question])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'catalogs.xml'
    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)
    assert len(root) == len(imported_elements) == 148
    # start test with fresh elements in db
    # breakpoint()
    elements = _test_helper_change_fields_elements(elements, fields_to_update=updated_fields, n=75)
    changed_elements = _test_helper_filter_updated_and_changed(elements.values(), updated_fields=updated_fields)
    imported_elements = import_elements(elements)
    imported_and_changed = _test_helper_filter_updated_and_changed(imported_elements, updated_fields=updated_fields)
    assert len(imported_elements) == 148
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
        assert test[ELEMENT_DIFF_FIELD_NAME] == imported[ELEMENT_DIFF_FIELD_NAME]


def test_create_sections(db, settings):
    delete_all_objects([Section, Page, QuestionSet, Question])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'sections.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
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

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 146
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


@pytest.mark.parametrize('updated_fields', fields_to_be_changed)
def test_update_sections_with_changed_fields(db, settings, updated_fields):
    delete_all_objects([Catalog, Section, Page, QuestionSet, Question])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'sections.xml'
    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)
    assert len(root) == len(imported_elements) == 146
    # start test with fresh elements in db

    elements = _test_helper_change_fields_elements(elements, fields_to_update=updated_fields, n=75)
    changed_elements = _test_helper_filter_updated_and_changed(elements.values(), updated_fields=updated_fields)
    imported_elements = import_elements(elements)
    imported_and_changed = _test_helper_filter_updated_and_changed(imported_elements, updated_fields=updated_fields)
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
        assert test[ELEMENT_DIFF_FIELD_NAME] == imported[ELEMENT_DIFF_FIELD_NAME]


def test_create_pages(db, settings):
    delete_all_objects([Page, QuestionSet, Question])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'pages.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 140
    assert Page.objects.count() == 48
    assert QuestionSet.objects.count() == 3
    assert Question.objects.count() == 89
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_pages(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'pages.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 140
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


@pytest.mark.parametrize('updated_fields', fields_to_be_changed)
def test_update_pages_with_changed_fields(db, settings, updated_fields):
    delete_all_objects([Catalog, Section, Page, QuestionSet, Question])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'pages.xml'
    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)
    assert len(root) == len(imported_elements) == 140
    # start test with fresh elements in db
    elements = _test_helper_change_fields_elements(elements, fields_to_update=updated_fields, n=75)
    changed_elements = _test_helper_filter_updated_and_changed(elements.values(), updated_fields=updated_fields)
    imported_elements = import_elements(elements)
    imported_and_changed = _test_helper_filter_updated_and_changed(imported_elements, updated_fields=updated_fields)
    assert len(imported_elements) == 140
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
        assert test[ELEMENT_DIFF_FIELD_NAME] == imported[ELEMENT_DIFF_FIELD_NAME]


def test_create_questionsets(db, settings):
    delete_all_objects([Page, QuestionSet, Question])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questionsets.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == 10  # two questionsets appear twice in the export file
    assert len(imported_elements) == 8
    assert QuestionSet.objects.count() == 3
    assert Question.objects.count() == 5
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_questionsets(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questionsets.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == 10  # two questionsets appear twice in the export file
    assert len(imported_elements) == 8
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


@pytest.mark.parametrize('updated_fields', fields_to_be_changed)
def test_update_questionsets_with_changed_fields(db, settings, updated_fields):
    delete_all_objects([Catalog, Section, Page, QuestionSet, Question])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questionsets.xml'
    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)
    assert len(root) == 10  # two questionsets appear twice in the export file
    assert len(imported_elements) == 8
    # start test with fresh elements in db
    elements = _test_helper_change_fields_elements(elements, fields_to_update=updated_fields, n=5)
    changed_elements = _test_helper_filter_updated_and_changed(elements.values(), updated_fields=updated_fields)
    imported_elements = import_elements(elements)
    imported_and_changed = _test_helper_filter_updated_and_changed(imported_elements, updated_fields=updated_fields)
    assert len(imported_elements) == 8
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
        assert test[ELEMENT_DIFF_FIELD_NAME] == imported[ELEMENT_DIFF_FIELD_NAME]


def test_create_questions(db, settings):
    delete_all_objects([Page, QuestionSet, Question])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questions.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 89
    assert Question.objects.count() == 89
    assert all(element['created'] is True for element in imported_elements)
    assert all(element['updated'] is False for element in imported_elements)


def test_update_questions(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questions.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 89
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)


@pytest.mark.parametrize('updated_fields', fields_to_be_changed)
def test_update_questions_with_changed_fields(db, settings, updated_fields):
    delete_all_objects([Catalog, Section, Page, QuestionSet, Question])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'questions.xml'
    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)
    assert len(root) == len(imported_elements) == 89
    # start test with fresh elements in db
    elements = _test_helper_change_fields_elements(elements, fields_to_update=updated_fields, n=45)
    changed_elements = _test_helper_filter_updated_and_changed(elements.values(), updated_fields=updated_fields)
    imported_elements = import_elements(elements)
    imported_and_changed = _test_helper_filter_updated_and_changed(imported_elements, updated_fields=updated_fields)
    assert len(imported_elements) == 89
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)
    assert len(imported_and_changed) == len(changed_elements)
    # compare two ordered lists with "updated_and_changed" dicts
    for test, imported in zip(changed_elements, imported_and_changed):
        assert test[ELEMENT_DIFF_FIELD_NAME] == imported[ELEMENT_DIFF_FIELD_NAME]


def test_create_legacy_questions(db, settings):
    delete_all_objects([Catalog, Section, Page, QuestionSet, Question])

    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'questions.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
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
    element_uris = {element['uri'] for _uri, element in elements.items() if element['uri'] != catalog.uri}
    assert descendant_uris == element_uris


def test_update_legacy_questions(db, settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'elements' / 'legacy' / 'questions.xml'

    elements, root = read_xml_and_parse_to_root_and_elements(xml_file)
    imported_elements = import_elements(elements)

    assert len(root) == len(imported_elements) == 147
    assert all(element['created'] is False for element in imported_elements)
    assert all(element['updated'] is True for element in imported_elements)

    # check that all elements ended up in the catalog
    catalog = Catalog.objects.prefetch_elements().first()
    descendant_uris = {element.uri for element in catalog.descendants}
    element_uris = {element['uri'] for _uri, element in elements.items() if element['uri'] != catalog.uri}
    assert descendant_uris == element_uris

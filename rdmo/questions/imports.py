import logging
import re

from django.core.exceptions import ValidationError
from rdmo.conditions.models import Condition
from rdmo.core.imports import set_lang_field
from rdmo.core.utils import get_languages
from rdmo.core.xml import filter_elements_by_type, flat_xml_to_elements
from rdmo.domain.models import Attribute
from rdmo.options.models import OptionSet

from .models import Catalog, Question, QuestionSet, Section
from .validators import (CatalogUniqueKeyValidator,
                         QuestionSetUniquePathValidator,
                         QuestionUniquePathValidator,
                         SectionUniquePathValidator)

log = logging.getLogger(__name__)


def import_questions(root, new_uri_prefix=None, new_key=None):
    update_set = None
    elements = flat_xml_to_elements(root)

    for element in filter_elements_by_type(elements, 'catalog'):
        update_set = import_catalog(element, new_uri_prefix, new_key)

    for element in filter_elements_by_type(elements, 'section'):
        section_uri = import_section(element, update_set)

    for element in filter_elements_by_type(elements, 'questionset'):
        questionset_uri = import_questionset(element, update_set=update_set, section_uri=section_uri)

    for element in filter_elements_by_type(elements, 'question'):
        import_question(element, update_set=update_set, questionset_uri=questionset_uri)


def import_catalog(element, new_uri_prefix=None, new_key=None):
    try:
        catalog = Catalog.objects.get(uri=element['uri'])
    except Catalog.DoesNotExist:
        log.info('Catalog not in db. Created with uri %s.', element['uri'])
        catalog = Catalog()

    catalog.uri_prefix = element['uri_prefix'] or ''
    catalog.key = element['key'] or ''
    catalog.comment = element['comment'] or ''

    catalog.order = element['order']

    update_set = None
    if new_key is not None:
        update_set = make_update_set(catalog, new_uri_prefix, new_key)
        catalog.id = None
        catalog.uri = update_set['new_catalog_uri']
        catalog.key = update_set['new_key']
        catalog.title_lang1 = update_set['new_catalog_title']
        catalog.title_lang2 = update_set['new_catalog_title']
    else:
        for lang_code, lang_string, lang_field in get_languages():
            set_lang_field(catalog, 'title', element, lang_code, lang_field)

    try:
        CatalogUniqueKeyValidator(catalog).validate()
    except ValidationError as e:
        log.info('Catalog not saving "%s" due to validation error (%s).', element['uri'], e)
    else:
        log.info('Catalog saving to "%s".', element['uri'])
        catalog.save()
    return update_set


def import_section(element, update_set=None):
    try:
        section = Section.objects.get(uri=element['uri'])
    except Section.DoesNotExist:
        log.info('Section not in db. Created with uri %s.', element['uri'])
        section = Section()

    try:
        if update_set is None:
            section.catalog = Catalog.objects.get(uri=element['catalog'])
            section.uri_prefix = element['uri_prefix'] or ''
            section.key = element['key'] or ''
            section.comment = element['comment'] or ''
        else:
            section.id = None
            section.catalog = Catalog.objects.get(uri=update_set['new_catalog_uri'])
            section.uri = update_set['new_catalog_uri'] + '/' + section.key
            section.uri_prefix = update_set['new_uri_prefix']
            section.path = section.build_path(section.key, section.catalog)
    except Catalog.DoesNotExist:
        log.info('Catalog not in db. Skipping.')
        return

    section.order = element['order']

    for lang_code, lang_string, lang_field in get_languages():
        set_lang_field(section, 'title', element, lang_code, lang_field)

    try:
        SectionUniquePathValidator(section).validate()
    except ValidationError as e:
        log.info('Section not saving "%s" due to validation error (%s).', section.uri, e)
    else:
        log.info('Section saving to "%s".', element['uri'])
        return section.save()


def import_questionset(element, update_set=None, section_uri=None):
    try:
        questionset = QuestionSet.objects.get(uri=element['uri'])
    except QuestionSet.DoesNotExist:
        log.info('QuestionSet not in db. Created with uri %s.', element['uri'])
        questionset = QuestionSet()

    try:
        if update_set is None:
            questionset.section = Section.objects.get(uri=element['section'])
            questionset.uri_prefix = element['uri_prefix'] or ''
            questionset.key = element['key'] or ''
            questionset.comment = element['comment'] or ''
        else:
            questionset.id = None
            questionset.section = Section.objects.get(uri=section_uri)
            questionset.uri = update_set['new_catalog_uri']
            questionset.uri_prefix = update_set['new_uri_prefix']
            questionset.key = update_set['new_catalog_title']
            questionset.path = questionset.build_path(questionset.key, questionset.section)
    except Section.DoesNotExist:
        log.info('Section not in db. Skipping.')
        return

    if element['attribute']:
        try:
            questionset.attribute = Attribute.objects.get(uri=element['attribute'])
        except Attribute.DoesNotExist:
            pass

    questionset.is_collection = element['is_collection']
    questionset.order = element['order']

    for lang_code, lang_string, lang_field in get_languages():
        set_lang_field(questionset, 'title', element, lang_code, lang_field)
        set_lang_field(questionset, 'help', element, lang_code, lang_field)
        set_lang_field(questionset, 'verbose_name', element, lang_code, lang_field)
        set_lang_field(questionset, 'verbose_name_plural', element, lang_code, lang_field)

    try:
        QuestionSetUniquePathValidator(questionset).validate()
    except ValidationError as e:
        log.info('QuestionSet not saving "%s" due to validation error (%s).', element['uri'], e)
    else:
        log.info('QuestionSet saving to "%s".', element['uri'])
        return questionset.save()

    questionset.conditions.clear()
    if element['conditions'] is not None:
        for condition in element['conditions']:
            try:
                questionset.conditions.add(Condition.objects.get(uri=condition))
            except Condition.DoesNotExist:
                pass


def import_question(element, update_set=None, questionset_uri=None):
    try:
        question = Question.objects.get(uri=element['uri'])
    except Question.DoesNotExist:
        log.info('QuestionSet not in db. Created with uri %s.', element['uri'])
        question = Question()

    try:
        if update_set is None:
            question.questionset = QuestionSet.objects.get(uri=element['questionset'])
            question.uri_prefix = element['uri_prefix'] or ''
            question.key = element['key'] or ''
            question.comment = element['comment'] or ''
        else:
            question.id = None
            question.questionset = QuestionSet.objects.get(uri=questionset_uri)
            question.uri = update_set['new_catalog_uri']
            question.uri_prefix = update_set['new_uri_prefix']
            question.key = update_set['new_catalog_title']
            question.path = question.build_path(question.key, question.questionset)
    except QuestionSet.DoesNotExist:
        log.info('QuestionSet not in db. Skipping.')
        return

    if element['attribute']:
        try:
            question.attribute = Attribute.objects.get(uri=element['attribute'])
        except Attribute.DoesNotExist:
            pass

    question.is_collection = element['is_collection']
    question.order = element['order']

    for lang_code, lang_string, lang_field in get_languages():
        set_lang_field(question, 'text', element, lang_code, lang_field)
        set_lang_field(question, 'help', element, lang_code, lang_field)
        set_lang_field(question, 'verbose_name', element, lang_code, lang_field)
        set_lang_field(question, 'verbose_name_plural', element, lang_code, lang_field)

    question.widget_type = element['widget_type'] or ''
    question.value_type = element['value_type'] or ''
    question.maximum = element['maximum']
    question.minimum = element['minimum']
    question.step = element['step']
    question.unit = element['unit'] or ''

    try:
        QuestionUniquePathValidator(question).validate()
    except ValidationError as e:
        log.info('Question not saving "%s" due to validation error (%s).', element['uri'], e)
    else:
        log.info('Question saving to "%s".', element['uri'])
        question.save()

    question.conditions.clear()
    if element['conditions'] is not None:
        for condition in element['conditions']:
            try:
                question.conditions.add(Condition.objects.get(uri=condition))
            except Condition.DoesNotExist:
                pass

    question.optionsets.clear()
    if element['optionsets'] is not None:
        for condition in element['optionsets']:
            try:
                question.optionsets.add(OptionSet.objects.get(uri=condition))
            except OptionSet.DoesNotExist:
                pass


def make_update_set(catalog, new_uri_prefix, new_title):
    update_set = {}
    update_set['uri_prefix'] = catalog.uri_prefix
    new_key = ''.join(
        re.findall(r'[a-z0-9-_]+', new_title.replace(' ', '_').lower()))
    update_set['new_key'] = new_key
    update_set['new_catalog_title'] = new_title
    update_set['new_uri_prefix'] = new_uri_prefix
    update_set['new_catalog_uri'] = re.search(
        r'^.*\/questions\/', catalog.uri
    ).group(0) + update_set['new_key']
    return update_set

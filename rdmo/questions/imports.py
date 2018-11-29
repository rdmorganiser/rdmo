import logging

from django.core.exceptions import ValidationError


from rdmo.core.xml import flat_xml_to_elements, filter_elements_by_type

from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute
from rdmo.options.models import OptionSet

from .models import Catalog, Section, QuestionSet, Question
from .validators import (
    CatalogUniqueKeyValidator,
    QuestionSetUniquePathValidator,
    QuestionUniquePathValidator,
    SectionUniquePathValidator
)

log = logging.getLogger(__name__)


def import_questions(root):
    elements = flat_xml_to_elements(root)

    for element in filter_elements_by_type(elements, 'catalog'):
        import_catalog(element)

    for element in filter_elements_by_type(elements, 'section'):
        import_section(element)

    for element in filter_elements_by_type(elements, 'questionset'):
        import_questionset(element)

    for element in filter_elements_by_type(elements, 'question'):
        import_question(element)


def import_catalog(element):
    try:
        catalog = Catalog.objects.get(uri=element['uri'])
    except Catalog.DoesNotExist:
        log.info('Catalog not in db. Created with uri %s.', element['uri'])
        catalog = Catalog()

    catalog.uri_prefix = element['uri_prefix']
    catalog.key = element['key']
    catalog.comment = element['comment']

    catalog.order = element['order']
    catalog.title_en = element['title_en']
    catalog.title_de = element['title_de']

    try:
        CatalogUniqueKeyValidator(catalog).validate()
    except ValidationError as e:
        log.info('Catalog not saving "%s" due to validation error (%s).', element['uri'], e)
        pass
    else:
        log.info('Catalog saving to "%s".', element['uri'])
        catalog.save()


def import_section(element):
    try:
        section = Section.objects.get(uri=element['uri'])
    except Section.DoesNotExist:
        log.info('Section not in db. Created with uri %s.', element['uri'])
        section = Section()

    try:
        section.catalog = Catalog.objects.get(uri=element['catalog'])
    except Catalog.DoesNotExist:
        log.info('Catalog not in db. Skipping.')
        return

    section.uri_prefix = element['uri_prefix']
    section.key = element['key']
    section.comment = element['comment']

    section.order = element['order']
    section.title_en = element['title_en']
    section.title_de = element['title_de']

    try:
        SectionUniquePathValidator(section).validate()
    except ValidationError as e:
        log.info('Section not saving "%s" due to validation error (%s).', element['uri'], e)
        pass
    else:
        log.info('Section saving to "%s".', element['uri'])
        section.save()


def import_questionset(element):
    try:
        questionset = QuestionSet.objects.get(uri=element['uri'])
    except QuestionSet.DoesNotExist:
        log.info('QuestionSet not in db. Created with uri %s.', element['uri'])
        questionset = QuestionSet()

    try:
        questionset.section = Section.objects.get(uri=element['section'])
    except Section.DoesNotExist:
        log.info('Section not in db. Skipping.')
        return

    questionset.uri_prefix = element['uri_prefix']
    questionset.key = element['key']
    questionset.comment = element['comment']

    if element['attribute']:
        try:
            questionset.attribute = Attribute.objects.get(uri=element['attribute'])
        except Attribute.DoesNotExist:
            pass

    questionset.is_collection = element['is_collection']
    questionset.order = element['order']
    questionset.title_en = element['title_en'] or ''
    questionset.title_de = element['title_de'] or ''
    questionset.help_en = element['help_en'] or ''
    questionset.help_de = element['help_de'] or ''
    questionset.verbose_name_en = element['verbose_name_en'] or ''
    questionset.verbose_name_de = element['verbose_name_de'] or ''
    questionset.verbose_name_plural_en = element['verbose_name_plural_en'] or ''
    questionset.verbose_name_plural_de = element['verbose_name_plural_de'] or ''

    try:
        QuestionSetUniquePathValidator(questionset).validate()
    except ValidationError as e:
        log.info('QuestionSet not saving "%s" due to validation error (%s).', element['uri'], e)
        pass
    else:
        log.info('QuestionSet saving to "%s".', element['uri'])
        questionset.save()

    questionset.conditions.clear()
    if element['conditions'] is not None:
        for condition in element['conditions']:
            try:
                questionset.conditions.add(Condition.objects.get(uri=condition))
            except Condition.DoesNotExist:
                pass


def import_question(element):
    try:
        question = Question.objects.get(uri=element['uri'])
    except Question.DoesNotExist:
        log.info('QuestionSet not in db. Created with uri %s.', element['uri'])
        question = Question()

    try:
        question.questionset = QuestionSet.objects.get(uri=element['questionset'])
    except QuestionSet.DoesNotExist:
        log.info('QuestionSet not in db. Skipping.')
        return

    question.uri_prefix = element['uri_prefix']
    question.key = element['key']
    question.comment = element['comment']

    if element['attribute']:
        try:
            question.attribute = Attribute.objects.get(uri=element['attribute'])
        except Attribute.DoesNotExist:
            pass

    question.is_collection = element['is_collection']
    question.order = element['order']
    question.text_en = element['text_en'] or ''
    question.text_de = element['text_de'] or ''
    question.help_en = element['help_en'] or ''
    question.help_de = element['help_de'] or ''
    question.verbose_name_en = element['verbose_name_en'] or ''
    question.verbose_name_de = element['verbose_name_de'] or ''
    question.verbose_name_plural_en = element['verbose_name_plural_en'] or ''
    question.verbose_name_plural_de = element['verbose_name_plural_de'] or ''
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
        pass
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

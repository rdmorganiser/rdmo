import logging

from django.contrib.sites.models import Site
from rdmo.conditions.models import Condition
from rdmo.core.imports import (get_instance, get_m2m_instances,
                               set_common_fields, set_foreign_field,
                               set_lang_field, set_temporary_fields,
                               validate_instance)
from rdmo.domain.models import Attribute
from rdmo.options.models import OptionSet

from .models import Catalog, Question, QuestionSet, Section
from .validators import (CatalogUniqueKeyValidator,
                         QuestionSetUniquePathValidator,
                         QuestionUniquePathValidator,
                         SectionUniquePathValidator)

logger = logging.getLogger(__name__)


def import_catalog(element, save=[]):
    catalog = get_instance(element, Catalog)

    set_common_fields(catalog, element)
    set_temporary_fields(catalog, element)

    catalog.order = element.get('order')

    set_lang_field(catalog, 'title', element)

    validate_instance(catalog, CatalogUniqueKeyValidator)

    if catalog.uri in save:
        if catalog.id:
            logger.info('Catalog created with uri %s.', element.get('uri'))
        else:
            logger.info('Catalog %s updated.', element.get('uri'))

        catalog.save()
        catalog.sites.add(Site.objects.get_current())

    return catalog


def import_section(element, save=[]):
    section = get_instance(element, Section)

    set_common_fields(section, element)
    set_temporary_fields(section, element)

    set_foreign_field(section, 'catalog', element, Catalog)

    section.order = element.get('order')

    set_lang_field(section, 'title', element)

    validate_instance(section, SectionUniquePathValidator)

    if section.uri in save:
        if section.id:
            logger.info('Section created with uri %s.', element.get('uri'))
        else:
            logger.info('Section %s updated.', element.get('uri'))

        section.save()

    return section


def import_questionset(element, save=[]):
    questionset = get_instance(element, QuestionSet)

    set_common_fields(questionset, element)
    set_temporary_fields(questionset, element)

    set_foreign_field(questionset, 'section', element, Section)
    set_foreign_field(questionset, 'attribute', element, Attribute)

    questionset.is_collection = element.get('is_collection')
    questionset.order = element.get('order')

    set_lang_field(questionset, 'title', element)
    set_lang_field(questionset, 'help', element)
    set_lang_field(questionset, 'verbose_name', element)
    set_lang_field(questionset, 'verbose_name_plural', element)

    conditions = get_m2m_instances(questionset, 'conditions', element, Condition)

    validate_instance(questionset, QuestionSetUniquePathValidator)

    if questionset.uri in save:
        if questionset.id:
            logger.info('QuestionSet created with uri %s.', element.get('uri'))
        else:
            logger.info('QuestionSet %s updated.', element.get('uri'))

        questionset.save()
        questionset.conditions.set(conditions)

    return questionset


def import_question(element, save=[]):
    question = get_instance(element, Question)

    set_common_fields(question, element)
    set_temporary_fields(question, element)

    set_foreign_field(question, 'questionset', element, QuestionSet)
    set_foreign_field(question, 'attribute', element, Attribute)

    question.is_collection = element.get('is_collection')
    question.order = element.get('order')

    set_lang_field(question, 'text', element)
    set_lang_field(question, 'help', element)
    set_lang_field(question, 'verbose_name', element)
    set_lang_field(question, 'verbose_name_plural', element)

    question.widget_type = element.get('widget_type') or ''
    question.value_type = element.get('value_type') or ''
    question.maximum = element.get('maximum')
    question.minimum = element.get('minimum')
    question.step = element.get('step')
    question.unit = element.get('unit') or ''

    conditions = get_m2m_instances(question, 'conditions', element, Condition)
    optionsets = get_m2m_instances(question, 'optionsets', element, OptionSet)

    validate_instance(question, QuestionUniquePathValidator)

    if question.uri in save:
        if question.id:
            logger.info('Question created with uri %s.', element.get('uri'))
        else:
            logger.info('Question %s updated.', element.get('uri'))

        question.save()
        question.conditions.set(conditions)
        question.optionsets.set(optionsets)

    return question

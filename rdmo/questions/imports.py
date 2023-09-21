import logging

from django.contrib.sites.models import Site

from rdmo.core.imports import (
    check_permissions,
    set_common_fields,
    set_foreign_field,
    set_lang_field,
    set_m2m_instances,
    set_m2m_through_instances,
    set_reverse_m2m_through_instance,
    validate_instance,
)

from .models import Catalog, Page, Question, QuestionSet, Section
from .utils import get_widget_types
from .validators import (
    CatalogLockedValidator,
    CatalogUniqueURIValidator,
    PageLockedValidator,
    PageUniqueURIValidator,
    QuestionLockedValidator,
    QuestionSetLockedValidator,
    QuestionSetUniqueURIValidator,
    QuestionUniqueURIValidator,
    SectionLockedValidator,
    SectionUniqueURIValidator,
)

logger = logging.getLogger(__name__)


def import_catalog(element, save=False, user=None):
    try:
        catalog = Catalog.objects.get(uri=element.get('uri'))
    except Catalog.DoesNotExist:
        catalog = Catalog()

    set_common_fields(catalog, element)

    catalog.order = element.get('order') or 0

    set_lang_field(catalog, 'title', element)
    set_lang_field(catalog, 'help', element)

    catalog.available = element.get('available', True)

    validate_instance(catalog, element, CatalogLockedValidator, CatalogUniqueURIValidator)

    check_permissions(catalog, element, user)

    if save and not element.get('errors'):
        if catalog.id:
            element['updated'] = True
            logger.info('Catalog %s updated.', element.get('uri'))
        else:
            element['created'] = True
            logger.info('Catalog created with uri %s.', element.get('uri'))

        catalog.save()
        set_m2m_through_instances(catalog, 'sections', element, 'catalog', 'section', 'catalog_sections')
        catalog.sites.add(Site.objects.get_current())
        catalog.editors.add(Site.objects.get_current())

    return catalog


def import_section(element, save=False, user=None):
    try:
        section = Section.objects.get(uri=element.get('uri'))
    except Section.DoesNotExist:
        section = Section()

    set_common_fields(section, element)

    set_lang_field(section, 'title', element)

    validate_instance(section, element, SectionLockedValidator, SectionUniqueURIValidator)

    check_permissions(section, element, user)

    if save and not element.get('errors'):
        if section.id:
            element['updated'] = True
            logger.info('Section %s updated.', element.get('uri'))
        else:
            element['created'] = True
            logger.info('Section created with uri %s.', element.get('uri'))

        section.save()
        set_reverse_m2m_through_instance(section, 'catalog', element, 'section', 'catalog', 'section_catalogs')
        set_m2m_through_instances(section, 'pages', element, 'section', 'page', 'section_pages')
        section.editors.add(Site.objects.get_current())

    return section


def import_page(element, save=False, user=None):
    try:
        page = Page.objects.get(uri=element.get('uri'))
    except Page.DoesNotExist:
        page = Page()

    set_common_fields(page, element)
    set_foreign_field(page, 'attribute', element)

    page.is_collection = element.get('is_collection') or False

    set_lang_field(page, 'title', element)
    set_lang_field(page, 'help', element)
    set_lang_field(page, 'verbose_name', element)
    set_lang_field(page, 'verbose_name_plural', element)

    validate_instance(page, element, PageLockedValidator, PageUniqueURIValidator)

    check_permissions(page, element, user)

    if save and not element.get('errors'):
        if page.id:
            element['updated'] = True
            logger.info('QuestionSet %s updated.', element.get('uri'))
        else:
            element['created'] = True
            logger.info('QuestionSet created with uri %s.', element.get('uri'))

        page.save()
        set_m2m_instances(page, 'conditions', element)
        set_reverse_m2m_through_instance(page, 'section', element, 'page', 'section', 'page_sections')
        set_m2m_through_instances(page, 'questionsets', element, 'page', 'questionset', 'page_questionsets')
        set_m2m_through_instances(page, 'questions', element, 'page', 'question', 'page_questions')
        page.editors.add(Site.objects.get_current())

    return page


def import_questionset(element, save=False, user=None):
    try:
        questionset = QuestionSet.objects.get(uri=element.get('uri'))
    except QuestionSet.DoesNotExist:
        questionset = QuestionSet()

    set_common_fields(questionset, element)
    set_foreign_field(questionset, 'attribute', element)

    questionset.is_collection = element.get('is_collection') or False

    set_lang_field(questionset, 'title', element)
    set_lang_field(questionset, 'help', element)
    set_lang_field(questionset, 'verbose_name', element)
    set_lang_field(questionset, 'verbose_name_plural', element)

    validate_instance(questionset, element, QuestionSetLockedValidator, QuestionSetUniqueURIValidator)

    check_permissions(questionset, element, user)

    if save and not element.get('errors'):
        if questionset.id:
            element['updated'] = True
            logger.info('QuestionSet %s updated.', element.get('uri'))
        else:
            element['created'] = True
            logger.info('QuestionSet created with uri %s.', element.get('uri'))

        questionset.save()
        set_m2m_instances(questionset, 'conditions', element)
        set_reverse_m2m_through_instance(questionset, 'page', element, 'questionset', 'page', 'questionset_pages')
        set_reverse_m2m_through_instance(questionset, 'questionset', element, 'questionset', 'parent', 'questionset_parents')  # noqa: E501
        set_m2m_through_instances(questionset, 'questionsets', element, 'parent', 'questionset', 'questionset_questionsets')  # noqa: E501
        set_m2m_through_instances(questionset, 'questions', element, 'questionset', 'question', 'questionset_questions')
        questionset.editors.add(Site.objects.get_current())

    return questionset


def import_question(element, save=False, user=None):
    try:
        question = Question.objects.get(uri=element.get('uri'))
    except Question.DoesNotExist:
        question = Question()

    set_common_fields(question, element)
    set_foreign_field(question, 'attribute', element)

    question.is_collection = element.get('is_collection') or False
    question.is_optional = element.get('is_optional') or False

    set_lang_field(question, 'text', element)
    set_lang_field(question, 'help', element)
    set_lang_field(question, 'default_text', element)
    set_lang_field(question, 'verbose_name', element)
    set_lang_field(question, 'verbose_name_plural', element)

    set_foreign_field(question, 'default_option', element)

    question.default_external_id = element.get('default_external_id') or ''

    if element.get('widget_type') in get_widget_types():
        question.widget_type = element.get('widget_type')
    else:
        question.widget_type = 'text'

    question.value_type = element.get('value_type') or ''
    question.maximum = element.get('maximum')
    question.minimum = element.get('minimum')
    question.step = element.get('step')
    question.unit = element.get('unit') or ''
    question.width = element.get('width')

    validate_instance(question, element, QuestionLockedValidator, QuestionUniqueURIValidator)

    check_permissions(question, element, user)

    if save and not element.get('errors'):
        if question.id:
            element['updated'] = True
            logger.info('Question %s updated.', element.get('uri'))
        else:
            element['created'] = True
            logger.info('Question created with uri %s.', element.get('uri'))

        question.save()
        set_reverse_m2m_through_instance(question, 'page', element, 'question', 'page', 'question_pages')
        set_reverse_m2m_through_instance(question, 'questionset', element, 'question', 'questionset', 'question_questionsets')  # noqa: E501
        set_m2m_instances(question, 'conditions', element)
        set_m2m_instances(question, 'optionsets', element)
        question.editors.add(Site.objects.get_current())

    return question

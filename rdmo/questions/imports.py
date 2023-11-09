import logging

from django.contrib.sites.models import Site

from rdmo.core.imports import (
    check_permissions,
    get_or_return_instance,
    make_import_info_msg,
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

    catalog, _created = get_or_return_instance(Catalog, uri=element.get('uri'))
    element['created'] = _created
    element['updated'] = not _created

    _msg = make_import_info_msg(catalog._meta.verbose_name, _created, uri=element.get('uri'))

    set_common_fields(catalog, element)

    catalog.order = element.get('order') or 0

    set_lang_field(catalog, 'title', element)
    set_lang_field(catalog, 'help', element)

    catalog.available = element.get('available', True)

    validate_instance(catalog, element, CatalogLockedValidator, CatalogUniqueURIValidator)

    check_permissions(catalog, element, user)

    if element.get('errors'):
        return catalog

    if save:
        logger.debug(_msg)
        catalog.save()
        set_m2m_through_instances(catalog, 'sections', element, 'catalog', 'section', 'catalog_sections')
        catalog.sites.add(Site.objects.get_current())
        catalog.editors.add(Site.objects.get_current())

    return catalog


def import_section(element, save=False, user=None):

    section, _created = get_or_return_instance(Section, uri=element.get('uri'))
    element['created'] = _created
    element['updated'] = not _created

    _msg = make_import_info_msg(section._meta.verbose_name, _created, uri=element.get('uri'))

    set_common_fields(section, element)

    set_lang_field(section, 'title', element)
    set_lang_field(section, 'short_title', element)

    validate_instance(section, element, SectionLockedValidator, SectionUniqueURIValidator)

    check_permissions(section, element, user)

    if element.get('errors'):
        return section

    if save:
        logger.info(_msg)
        section.save()
        set_reverse_m2m_through_instance(section, 'catalog', element, 'section', 'catalog', 'section_catalogs')
        set_m2m_through_instances(section, 'pages', element, 'section', 'page', 'section_pages')
        section.editors.add(Site.objects.get_current())

    return section


def import_page(element, save=False, user=None):

    page, _created = get_or_return_instance(Page, uri=element.get('uri'))
    element['created'] = _created
    element['updated'] = not _created

    _msg = make_import_info_msg(page._meta.verbose_name, _created, uri=element.get('uri'))

    set_common_fields(page, element)
    set_foreign_field(page, 'attribute', element)

    page.is_collection = element.get('is_collection') or False

    set_lang_field(page, 'title', element)
    set_lang_field(page, 'short_title', element)
    set_lang_field(page, 'help', element)
    set_lang_field(page, 'verbose_name', element)

    validate_instance(page, element, PageLockedValidator, PageUniqueURIValidator)

    check_permissions(page, element, user)

    if element.get('errors'):
        return page

    if save:
        logger.info(_msg)
        page.save()
        set_m2m_instances(page, 'conditions', element)
        set_reverse_m2m_through_instance(page, 'section', element, 'page', 'section', 'page_sections')
        set_m2m_through_instances(page, 'questionsets', element, 'page', 'questionset', 'page_questionsets')
        set_m2m_through_instances(page, 'questions', element, 'page', 'question', 'page_questions')
        page.editors.add(Site.objects.get_current())

    return page


def import_questionset(element, save=False, user=None):

    questionset, _created = get_or_return_instance(QuestionSet, uri=element.get('uri'))
    element['created'] = _created
    element['updated'] = not _created

    _msg = make_import_info_msg(questionset._meta.verbose_name, _created, uri=element.get('uri'))

    set_common_fields(questionset, element)
    set_foreign_field(questionset, 'attribute', element)

    questionset.is_collection = element.get('is_collection') or False

    set_lang_field(questionset, 'title', element)
    set_lang_field(questionset, 'help', element)
    set_lang_field(questionset, 'verbose_name', element)

    validate_instance(questionset, element, QuestionSetLockedValidator, QuestionSetUniqueURIValidator)

    check_permissions(questionset, element, user)

    if element.get('errors'):
        return questionset

    if save:
        logger.info(_msg)
        questionset.save()
        set_m2m_instances(questionset, 'conditions', element)
        set_reverse_m2m_through_instance(questionset, 'page', element, 'questionset', 'page', 'questionset_pages')
        set_reverse_m2m_through_instance(questionset, 'questionset', element, 'questionset', 'parent', 'questionset_parents')  # noqa: E501
        set_m2m_through_instances(questionset, 'questionsets', element, 'parent', 'questionset', 'questionset_questionsets')  # noqa: E501
        set_m2m_through_instances(questionset, 'questions', element, 'questionset', 'question', 'questionset_questions')
        questionset.editors.add(Site.objects.get_current())

    return questionset


def import_question(element, save=False, user=None):

    question, _created = get_or_return_instance(Question, uri=element.get('uri'))
    element['created'] = _created
    element['updated'] = not _created

    _msg = make_import_info_msg(question._meta.verbose_name, _created, uri=element.get('uri'))

    set_common_fields(question, element)
    set_foreign_field(question, 'attribute', element)

    question.is_collection = element.get('is_collection') or False
    question.is_optional = element.get('is_optional') or False

    set_lang_field(question, 'text', element)
    set_lang_field(question, 'help', element)
    set_lang_field(question, 'default_text', element)
    set_lang_field(question, 'verbose_name', element)

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

    if element.get('errors'):
        return question

    if save:
        logger.info(_msg)
        question.save()
        set_reverse_m2m_through_instance(question, 'page', element, 'question', 'page', 'question_pages')
        set_reverse_m2m_through_instance(question, 'questionset', element, 'question', 'questionset', 'question_questionsets')  # noqa: E501
        set_m2m_instances(question, 'conditions', element)
        set_m2m_instances(question, 'optionsets', element)
        question.editors.add(Site.objects.get_current())

    return question

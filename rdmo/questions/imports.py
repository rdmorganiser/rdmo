import logging
from typing import Callable, Tuple

from django.contrib.sites.models import Site
from django.db import models

from rdmo.core.imports import (
    ElementImportHelper,
    set_m2m_instances,
    set_m2m_through_instances,
    set_reverse_m2m_through_instance,
    validate_instance,
)
from rdmo.questions.validators import (
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

from .models.catalog import Catalog
from .models.page import Page
from .models.question import Question
from .models.questionset import QuestionSet
from .models.section import Section
from .utils import get_widget_types

logger = logging.getLogger(__name__)


def import_catalog(
        instance: Catalog,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
        user: models.Model = None
    ):
    # check_permissions already done in management/import.py
    instance.order = element.get('order') or 0

    instance.available = element.get('available', True)

    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_m2m_through_instances(instance, 'sections', element, 'catalog', 'section', 'catalog_sections')
        instance.sites.add(Site.objects.get_current())
        instance.editors.add(Site.objects.get_current())

    return instance


def import_section(
        instance: Section,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
        user: models.Model = None
    ):
    # check_permissions already done in management/import.py
    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_reverse_m2m_through_instance(instance, 'catalog', element, 'section', 'catalog', 'section_catalogs')
        set_m2m_through_instances(instance, 'pages', element, 'section', 'page', 'section_pages')
        instance.editors.add(Site.objects.get_current())

    return instance


def import_page(
        instance: Page,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
        user: models.Model = None
    ):
    # lang_fields are already set in management/import.py
    # set_foreign_field are already set in management/import.py
    # check_permissions already done in management/import.py

    instance.is_collection = element.get('is_collection') or False

    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_m2m_instances(instance, 'conditions', element)
        set_reverse_m2m_through_instance(instance, 'section', element, 'page', 'section', 'page_sections')
        set_m2m_through_instances(instance, 'questionsets', element, 'page', 'questionset', 'page_questionsets')
        set_m2m_through_instances(instance, 'questions', element, 'page', 'question', 'page_questions')
        instance.editors.add(Site.objects.get_current())

    return instance


def import_questionset(
        instance: QuestionSet,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
        user: models.Model = None
    ):
    # lang_fields are already set in management/import.py
    # set_foreign_field are already set in management/import.py
    # check_permissions already done in management/import.py

    instance.is_collection = element.get('is_collection') or False

    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_m2m_instances(instance, 'conditions', element)
        set_reverse_m2m_through_instance(instance, 'page', element, 'questionset', 'page', 'questionset_pages')
        set_reverse_m2m_through_instance(instance, 'questionset', element, 'questionset', 'parent', 'questionset_parents')  # noqa: E501
        set_m2m_through_instances(instance, 'questionsets', element, 'parent', 'questionset', 'questionset_questionsets')  # noqa: E501
        set_m2m_through_instances(instance, 'questions', element, 'questionset', 'question', 'questionset_questions')
        instance.editors.add(Site.objects.get_current())

    return instance


def import_question(
        instance: Question,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
        user: models.Model = None
    ):
    # lang_fields are already set in management/import.py
    # set_foreign_fields are already set in management/import.py
    # check_permissions already done in management/import.py

    instance.is_collection = element.get('is_collection') or False
    instance.is_optional = element.get('is_optional') or False

    instance.default_external_id = element.get('default_external_id') or ''

    if element.get('widget_type') in get_widget_types():
        instance.widget_type = element.get('widget_type')
    else:
        instance.widget_type = 'text'

    instance.value_type = element.get('value_type') or ''
    instance.maximum = element.get('maximum')
    instance.minimum = element.get('minimum')
    instance.step = element.get('step')
    instance.unit = element.get('unit') or ''
    instance.width = element.get('width')

    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_reverse_m2m_through_instance(instance, 'page', element, 'question', 'page', 'question_pages')
        set_reverse_m2m_through_instance(instance, 'questionset', element, 'question', 'questionset', 'question_questionsets')  # noqa: E501
        set_m2m_instances(instance, 'conditions', element)
        set_m2m_instances(instance, 'optionsets', element)
        instance.editors.add(Site.objects.get_current())

    return instance


import_helper_catalog = ElementImportHelper(
    model="questions.catalog",
    import_func=import_catalog,
    validators=(CatalogLockedValidator, CatalogUniqueURIValidator),
    lang_fields=('help', 'title')
)

import_helper_section = ElementImportHelper(
    model="questions.section",
    import_func=import_section,
    validators=(SectionLockedValidator, SectionUniqueURIValidator),
    lang_fields=('title',)
)

import_helper_page = ElementImportHelper(
    model="questions.page",
    import_func=import_page,
    validators=(PageLockedValidator, PageUniqueURIValidator),
    lang_fields=('help', 'title', 'verbose_name'),
    foreign_fields=('attribute',)
)

import_helper_questionset = ElementImportHelper(
    model="questions.questionset",
    import_func=import_questionset,
    validators=(QuestionSetLockedValidator, QuestionSetUniqueURIValidator),
    lang_fields=('help', 'title', 'verbose_name'),
    foreign_fields=('attribute',)
)

import_helper_question = ElementImportHelper(
    model="questions.question",
    import_func=import_question,
    validators=(QuestionLockedValidator, QuestionUniqueURIValidator),
    lang_fields=('text', 'help', 'default_text', 'verbose_name'),
    foreign_fields=('attribute','default_option')
)

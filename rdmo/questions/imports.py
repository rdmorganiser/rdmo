import logging
from typing import Callable, Tuple

from rdmo.core.imports import (
    ElementImportHelper,
    set_m2m_instances,
    set_m2m_through_instances,
    set_reverse_m2m_through_instance,
    validate_instance,
)

from .models.catalog import Catalog
from .models.page import Page
from .models.question import Question
from .models.questionset import QuestionSet
from .models.section import Section
from .serializers.v1 import (
    CatalogSerializer,
    PageSerializer,
    QuestionSerializer,
    QuestionSetSerializer,
    SectionSerializer,
)
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


def import_catalog(
        instance: Catalog,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
    ):
    # check_permissions already done in management/import.py
    # extra_fields are set in management/import.py
    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_m2m_through_instances(instance, 'sections', element, 'catalog', 'section', 'catalog_sections')
        # sites and editors are added in management/import.py

    return instance


def import_section(
        instance: Section,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
    ):
    # check_permissions already done in management/import.py
    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_reverse_m2m_through_instance(instance, 'catalog', element, 'section', 'catalog', 'section_catalogs')
        set_m2m_through_instances(instance, 'pages', element, 'section', 'page', 'section_pages')
        # sites and editors are added in management/import.py

    return instance


def import_page(
        instance: Page,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
    ):
    # lang_fields are already set in management/import.py
    # set_foreign_field are already set in management/import.py
    # check_permissions already done in management/import.py
    # extra_fields are set in management/import.py
    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_m2m_instances(instance, 'conditions', element)
        set_reverse_m2m_through_instance(instance, 'section', element, 'page', 'section', 'page_sections')
        set_m2m_through_instances(instance, 'questionsets', element, 'page', 'questionset', 'page_questionsets')
        set_m2m_through_instances(instance, 'questions', element, 'page', 'question', 'page_questions')
        # sites and editors are added in management/import.py

    return instance


def import_questionset(
        instance: QuestionSet,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
    ):
    # lang_fields are already set in management/import.py
    # set_foreign_field are already set in management/import.py
    # check_permissions already done in management/import.py
    # extra_fields are set in management/import.py
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
        # sites and editors are added in management/import.py

    return instance


def import_question(
        instance: Question,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
    ):
    # lang_fields are already set in management/import.py
    # set_foreign_fields are already set in management/import.py
    # check_permissions already done in management/import.py
    # extra_fields are set in management/import.py
    validate_instance(instance, element, *validators)
    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_reverse_m2m_through_instance(instance, 'page', element, 'question', 'page', 'question_pages')
        set_reverse_m2m_through_instance(instance, 'questionset', element, 'question', 'questionset', 'question_questionsets')  # noqa: E501
        set_m2m_instances(instance, 'conditions', element)
        set_m2m_instances(instance, 'optionsets', element)
        # sites and editors are added in management/import.py

    return instance


import_helper_catalog = ElementImportHelper(
    model="questions.catalog",
    import_func=import_catalog,
    validators=(CatalogLockedValidator, CatalogUniqueURIValidator),
    lang_fields=('help', 'title'),
    serializer = CatalogSerializer,
    add_current_site_sites = True,
    extra_fields = ('order', 'available')
)

import_helper_section = ElementImportHelper(
    model="questions.section",
    import_func=import_section,
    validators=(SectionLockedValidator, SectionUniqueURIValidator),
    lang_fields=('title',),
    serializer = SectionSerializer
)

import_helper_page = ElementImportHelper(
    model="questions.page",
    import_func=import_page,
    validators=(PageLockedValidator, PageUniqueURIValidator),
    lang_fields=('help', 'title', 'verbose_name'),
    foreign_fields=('attribute',),
    serializer = PageSerializer,
    extra_fields = ('is_collection',)
)

import_helper_questionset = ElementImportHelper(
    model="questions.questionset",
    import_func=import_questionset,
    validators=(QuestionSetLockedValidator, QuestionSetUniqueURIValidator),
    lang_fields=('help', 'title', 'verbose_name'),
    foreign_fields=('attribute',),
    serializer = QuestionSetSerializer,
    extra_fields = ('is_collection',)
)

import_helper_question = ElementImportHelper(
    model="questions.question",
    import_func=import_question,
    validators=(QuestionLockedValidator, QuestionUniqueURIValidator),
    lang_fields=('text', 'help', 'default_text', 'verbose_name'),
    foreign_fields=('attribute','default_option'),
    serializer = QuestionSerializer,
    extra_fields = ('is_collection','is_optional', 'default_external_id', 'widget_type',
                    'value_type', 'maximum', 'minimum', 'step', 'unit','width')
)

from rdmo.core.import_helpers import ElementImportHelper, ExtraFieldHelper, ThroughInstanceMapper

from ..core.constants import VALUE_TYPE_TEXT
from .models import Catalog, Page, Question, QuestionSet, Section
from .utils import get_widget_type_or_default
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

import_helper_catalog = ElementImportHelper(
    model=Catalog,
    validators=(CatalogLockedValidator, CatalogUniqueURIValidator),
    lang_fields=('title', 'help'),
    extra_fields=(
        ExtraFieldHelper(field_name='order'),
        ExtraFieldHelper(field_name='available', overwrite_in_element=True),
    ),
    m2m_through_instance_fields=[
        ThroughInstanceMapper(
            field_name='sections', source_name='catalog',
            target_name='section', through_name='catalog_sections'
        )
    ],
    add_current_site_sites = True,
)

import_helper_section = ElementImportHelper(
    model=Section,
    validators=(SectionLockedValidator, SectionUniqueURIValidator),
    lang_fields=('title', 'short_title'),
    m2m_through_instance_fields=[
        ThroughInstanceMapper(
            field_name='pages', source_name='section',
            target_name='page', through_name='section_pages'
        )
    ],
    reverse_m2m_through_instance_fields=[
        ThroughInstanceMapper(
            field_name='catalog', source_name='section',
            target_name='catalog', through_name='section_catalogs'
        )
    ]
)

import_helper_page = ElementImportHelper(
    model=Page,
    validators=(PageLockedValidator, PageUniqueURIValidator),
    lang_fields=('help', 'title', 'verbose_name', 'short_title'),
    foreign_fields=('attribute',),
    extra_fields=(
        ExtraFieldHelper(field_name='is_collection'),
    ),
    m2m_instance_fields=('conditions', ),
    m2m_through_instance_fields=[
        ThroughInstanceMapper(
            field_name='questionsets', source_name='page',
            target_name='questionset', through_name='page_questionsets'
        ),
        ThroughInstanceMapper(
            field_name='questions', source_name='page',
            target_name='question', through_name='page_questions'
        )
    ],
    reverse_m2m_through_instance_fields=[
        ThroughInstanceMapper(
            field_name='section', source_name='page',
            target_name='section', through_name='page_sections'
        )
    ]
)

import_helper_questionset = ElementImportHelper(
    model=QuestionSet,
    validators=(QuestionSetLockedValidator, QuestionSetUniqueURIValidator),
    lang_fields=( 'title', 'help', 'verbose_name'),
    foreign_fields=('attribute',),
    extra_fields=(
        ExtraFieldHelper(field_name='is_collection'),
    ),
    m2m_instance_fields=('conditions', ),

    m2m_through_instance_fields=[
        ThroughInstanceMapper(
            field_name='questionsets', source_name='parent',
            target_name='questionset', through_name='questionset_questionsets'
        ),
        ThroughInstanceMapper(
            field_name='questions', source_name='questionset',
            target_name='question', through_name='questionset_questions'
        )
    ],
    reverse_m2m_through_instance_fields=[
        ThroughInstanceMapper(
            field_name='page', source_name='questionset',
            target_name='page', through_name='questionset_pages'
        ),
        ThroughInstanceMapper(
            field_name='questionset', source_name='questionset',
            target_name='parent', through_name='questionset_parents'
        )
    ]
)

import_helper_question = ElementImportHelper(
    model=Question,
    validators=(QuestionLockedValidator, QuestionUniqueURIValidator),
    lang_fields=('text', 'help', 'default_text', 'verbose_name'),
    foreign_fields=('attribute', 'default_option'),
    extra_fields=(
        ExtraFieldHelper(field_name='is_collection'),
        ExtraFieldHelper(field_name='is_optional'),
        ExtraFieldHelper(field_name='default_external_id', value=''),
        ExtraFieldHelper(field_name='widget_type', callback=get_widget_type_or_default),
        ExtraFieldHelper(field_name='value_type', value=VALUE_TYPE_TEXT),
        ExtraFieldHelper(field_name='minimum'),
        ExtraFieldHelper(field_name='maximum'),
        ExtraFieldHelper(field_name='step'),
        ExtraFieldHelper(field_name='unit', value=''),
        ExtraFieldHelper(field_name='width'),
    ),
    m2m_instance_fields=('conditions', 'optionsets'),
    reverse_m2m_through_instance_fields=[
        ThroughInstanceMapper(
            field_name='page', source_name='question',
            target_name='page', through_name='question_pages'
        ),
        ThroughInstanceMapper(
            field_name='questionset', source_name='question',
            target_name='questionset', through_name='question_questionsets'
        )
    ]
)

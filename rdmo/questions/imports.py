from rdmo.core.import_helpers import ElementImportHelper, ExtraFieldDefaultHelper, ThroughInstanceMapper

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
    model = Catalog,
    model_path="questions.catalog",
    validators=(CatalogLockedValidator, CatalogUniqueURIValidator),
    lang_fields=('help', 'title'),
    extra_fields = (
        ExtraFieldDefaultHelper(field_name='order'),
        ExtraFieldDefaultHelper(field_name='available'),
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
    model = Section,
    model_path="questions.section",
    validators=(SectionLockedValidator, SectionUniqueURIValidator),
    lang_fields=('title',),
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
    model = Page,
    model_path="questions.page",
    validators=(PageLockedValidator, PageUniqueURIValidator),
    lang_fields=('help', 'title', 'verbose_name'),
    foreign_fields=('attribute',),
    extra_fields = (
        ExtraFieldDefaultHelper(field_name='is_collection'),
    ),
    m2m_instance_fields = ('conditions', ),
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

import_helper_question = ElementImportHelper(
    model=Question,
    model_path="questions.question",
    validators=(QuestionLockedValidator, QuestionUniqueURIValidator),
    lang_fields=('text', 'help', 'default_text', 'verbose_name'),
    foreign_fields=('attribute', 'default_option'),
    extra_fields=(
        ExtraFieldDefaultHelper(field_name='is_collection'),
        ExtraFieldDefaultHelper(field_name='is_optional'),
        ExtraFieldDefaultHelper(field_name='default_external_id', value=''),
        ExtraFieldDefaultHelper(field_name='widget_type', callback=get_widget_type_or_default),
        ExtraFieldDefaultHelper(field_name='value_type', value=VALUE_TYPE_TEXT),
        ExtraFieldDefaultHelper(field_name='minimum'),
        ExtraFieldDefaultHelper(field_name='maximum'),
        ExtraFieldDefaultHelper(field_name='step'),
        ExtraFieldDefaultHelper(field_name='unit', value=''),
        ExtraFieldDefaultHelper(field_name='width'),
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
import_helper_questionset = ElementImportHelper(
    model = QuestionSet,
    model_path="questions.questionset",
    validators=(QuestionSetLockedValidator, QuestionSetUniqueURIValidator),
    lang_fields=('help', 'title', 'verbose_name'),
    foreign_fields=('attribute',),
    extra_fields=(
        ExtraFieldDefaultHelper(field_name='is_collection'),
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

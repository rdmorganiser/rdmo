from rdmo.core.imports import (
    ElementImportHelper,
)

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

import_helper_catalog = ElementImportHelper(
    model="questions.catalog",
    validators=(CatalogLockedValidator, CatalogUniqueURIValidator),
    lang_fields=('help', 'title'),
    serializer = CatalogSerializer,
    extra_fields = ('order', 'available'),
    m2m_through_instance_fields=[
        {'field_name': 'sections', 'source_name': 'catalog',
         'target_name': 'section', 'through_name': 'catalog_sections'}
    ],
    add_current_site_sites = True,
)

import_helper_section = ElementImportHelper(
    model="questions.section",
    validators=(SectionLockedValidator, SectionUniqueURIValidator),
    lang_fields=('title',),
    serializer = SectionSerializer,
    m2m_through_instance_fields=[
        {'field_name': 'pages', 'source_name': 'section',
         'target_name': 'page', 'through_name': 'section_pages'}
    ],
    reverse_m2m_through_instance_fields=[
        {'field_name': 'catalog', 'source_name': 'section',
         'target_name': 'catalog', 'through_name': 'section_catalogs'}
    ]
)


import_helper_page = ElementImportHelper(
    model="questions.page",
    validators=(PageLockedValidator, PageUniqueURIValidator),
    lang_fields=('help', 'title', 'verbose_name'),
    foreign_fields=('attribute',),
    serializer = PageSerializer,
    extra_fields = ('is_collection',),
    m2m_instance_fields = ('conditions', ),
    m2m_through_instance_fields=[
        {'field_name': 'questionsets', 'source_name': 'page',
         'target_name': 'questionset', 'through_name': 'page_questionsets'},
        {'field_name': 'questions', 'source_name': 'page',
         'target_name': 'question', 'through_name': 'page_questions'}
    ],
    reverse_m2m_through_instance_fields=[
        {'field_name': 'section', 'source_name': 'page',
         'target_name': 'section', 'through_name': 'page_sections'}
    ]
)


import_helper_questionset = ElementImportHelper(
    model="questions.questionset",
    validators=(QuestionSetLockedValidator, QuestionSetUniqueURIValidator),
    lang_fields=('help', 'title', 'verbose_name'),
    foreign_fields=('attribute',),
    serializer = QuestionSetSerializer,
    extra_fields = ('is_collection',),
    m2m_instance_fields = ('conditions', ),
    m2m_through_instance_fields=[
        {'field_name': 'questionsets', 'source_name': 'parent',
         'target_name': 'questionset', 'through_name': 'questionset_questionsets'},
        {'field_name': 'questions', 'source_name': 'questionset',
         'target_name': 'question', 'through_name': 'questionset_questions'}
    ],
    reverse_m2m_through_instance_fields=[
        {'field_name': 'page', 'source_name': 'questionset',
         'target_name': 'page', 'through_name': 'questionset_pages'},
        {'field_name': 'questionset', 'source_name': 'questionset',
         'target_name': 'parent', 'through_name': 'questionset_parents'}
    ]
)


import_helper_question = ElementImportHelper(
    model="questions.question",
    validators=(QuestionLockedValidator, QuestionUniqueURIValidator),
    lang_fields=('text', 'help', 'default_text', 'verbose_name'),
    foreign_fields=('attribute','default_option'),
    serializer=QuestionSerializer,
    extra_fields=('is_collection','is_optional', 'default_external_id', 'widget_type',
                    'value_type', 'maximum', 'minimum', 'step', 'unit','width'),
    m2m_instance_fields=('conditions', 'optionsets'),
    reverse_m2m_through_instance_fields=[
        {'field_name': 'page', 'source_name': 'question',
         'target_name': 'page', 'through_name': 'question_pages'},
        {'field_name': 'questionset', 'source_name': 'question',
         'target_name': 'questionset', 'through_name': 'question_questionsets'}
    ]
)

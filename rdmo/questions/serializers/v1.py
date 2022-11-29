from django.conf import settings
from rest_framework import serializers
from rest_framework.reverse import reverse

from rdmo.conditions.models import Condition
from rdmo.core.serializers import (SiteSerializer, ThroughModelSerializerMixin,
                                   TranslationSerializerMixin)
from rdmo.core.utils import get_language_warning
from rdmo.domain.models import Attribute
from rdmo.options.models import OptionSet

from ..models import (Catalog, CatalogSection, Page, PageQuestion,
                      PageQuestionSet, Question, QuestionSet,
                      QuestionSetQuestion, QuestionSetQuestionSet, Section,
                      SectionPage)
from ..utils import get_widget_type_choices
from ..validators import (CatalogLockedValidator, CatalogUniqueURIValidator,
                          PageLockedValidator, PageUniqueURIValidator,
                          QuestionLockedValidator, QuestionSetLockedValidator,
                          QuestionSetQuestionSetValidator,
                          QuestionSetUniqueURIValidator,
                          QuestionUniqueURIValidator, SectionLockedValidator,
                          SectionUniqueURIValidator)


class CatalogSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatalogSection
        fields = (
            'section',
            'order'
        )


class CatalogSerializer(ThroughModelSerializerMixin, TranslationSerializerMixin, serializers.ModelSerializer):

    uri_path = serializers.CharField(required=True)
    projects_count = serializers.IntegerField(read_only=True)

    sections = CatalogSectionSerializer(source='catalog_sections', read_only=False, required=False, many=True)

    class Meta:
        model = Catalog
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'order',
            'available',
            'sections',
            'sites',
            'groups',
            'projects_count'
        )
        trans_fields = (
            'title',
            'help'
        )
        through_fields = (
            'catalog_sections',
        )
        validators = (
            CatalogUniqueURIValidator(),
            CatalogLockedValidator()
        )


class SectionCatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatalogSection
        fields = (
            'catalog',
            'order'
        )


class SectionPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SectionPage
        fields = (
            'page',
            'order'
        )


class SectionSerializer(ThroughModelSerializerMixin, TranslationSerializerMixin, serializers.ModelSerializer):

    uri_path = serializers.CharField(required=True)

    catalogs = SectionCatalogSerializer(source='section_catalogs', read_only=False, required=False, many=True)
    pages = SectionPageSerializer(source='section_pages', read_only=False, required=False, many=True)

    class Meta:
        model = Section
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'catalogs',
            'pages'
        )
        trans_fields = (
            'title',
        )
        through_fields = (
            'section_catalogs',
            'section_pages'
        )
        validators = (
            SectionUniqueURIValidator(),
            SectionLockedValidator()
        )


class PageSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SectionPage
        fields = (
            'section',
            'order'
        )


class PageQuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = PageQuestionSet
        fields = (
            'questionset',
            'order'
        )


class PageQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PageQuestion
        fields = (
            'question',
            'order'
        )


class PageSerializer(ThroughModelSerializerMixin, TranslationSerializerMixin, serializers.ModelSerializer):

    uri_path = serializers.CharField(required=True)

    sections = PageSectionSerializer(source='page_sections', read_only=False, required=False, many=True)
    questionsets = PageQuestionSetSerializer(source='page_questionsets', read_only=False, required=False, many=True)
    questions = PageQuestionSerializer(source='page_questions', read_only=False, required=False, many=True)

    class Meta:
        model = Page
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'attribute',
            'is_collection',
            'sections',
            'questionsets',
            'questions',
            'conditions',
        )
        trans_fields = (
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
        )
        through_fields = (
            'page_sections',
            'page_questionsets',
            'page_questions'
        )
        validators = (
            PageUniqueURIValidator(),
            PageLockedValidator()
        )


class QuestionSetPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PageQuestionSet
        fields = (
            'page',
            'order'
        )


class QuestionSetParentSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSetQuestionSet
        fields = (
            'parent',
            'order'
        )


class QuestionSetQuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSetQuestionSet
        fields = (
            'questionset',
            'order'
        )


class QuestionSetQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSetQuestion
        fields = (
            'question',
            'order'
        )


class QuestionSetSerializer(ThroughModelSerializerMixin, TranslationSerializerMixin, serializers.ModelSerializer):

    uri_path = serializers.CharField(required=True)

    pages = QuestionSetPageSerializer(source='questionset_pages', read_only=False, required=False, many=True)
    parents = QuestionSetParentSerializer(source='questionset_parents', read_only=False, required=False, many=True)
    questionsets = QuestionSetQuestionSetSerializer(source='questionset_questionsets', read_only=False, required=False, many=True)
    questions = QuestionSetQuestionSerializer(source='questionset_questions', read_only=False, required=False, many=True)

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'attribute',
            'is_collection',
            'pages',
            'parents',
            'questionsets',
            'questions',
            'conditions',
        )
        trans_fields = (
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
        )
        through_fields = (
            'questionset_pages',
            'questionset_parents',
            'questionset_questionsets',
            'questionset_questions'
        )
        validators = (
            QuestionSetUniqueURIValidator(),
            QuestionSetQuestionSetValidator(),
            QuestionSetLockedValidator()
        )


class QuestionPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PageQuestion
        fields = (
            'page',
            'order'
        )


class QuestionQuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSetQuestion
        fields = (
            'questionset',
            'order'
        )


class QuestionSerializer(ThroughModelSerializerMixin, TranslationSerializerMixin, serializers.ModelSerializer):

    uri_path = serializers.CharField(required=True)
    widget_type = serializers.ChoiceField(choices=get_widget_type_choices(), required=True)

    pages = QuestionPageSerializer(source='question_pages', read_only=False, required=False, many=True)
    questionsets = QuestionQuestionSetSerializer(source='question_questionsets', read_only=False, required=False, many=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'attribute',
            'is_collection',
            'is_optional',
            'maximum',
            'minimum',
            'step',
            'default_option',
            'default_external_id',
            'widget_type',
            'value_type',
            'unit',
            'width',
            'pages',
            'questionsets',
            'optionsets',
            'conditions'
        )
        trans_fields = (
            'text',
            'help',
            'default_text',
            'verbose_name',
            'verbose_name_plural',
        )
        through_fields = (
            'question_pages',
            'question_questionsets'
        )
        validators = (
            QuestionUniqueURIValidator(),
            QuestionLockedValidator()
        )

    def to_internal_value(self, data):
        # handles an empty width, maximum, minimum, or step field
        for field in ['width', 'maximum', 'minimum', 'step']:
            if data.get(field) == '':
                data[field] = None

        return super().to_internal_value(data)


class CatalogIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = (
            'id',
            'title',
            'uri',
            'uri_prefix',
            'sites'
        )


class SectionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'title',
            'uri',
            'uri_prefix'
        )


class PageIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = (
            'id',
            'title',
            'uri',
            'uri_prefix'
        )


class QuestionSetIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'title',
            'uri',
            'uri_prefix'
        )


class QuestionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'text',
            'uri',
            'uri_prefix'
        )


class AttributeNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'uri'
        )


class OptionSetNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri'
        )


class ConditionNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'uri'
        )


class QuestionNestedSerializer(serializers.ModelSerializer):

    warning = serializers.SerializerMethodField()
    attribute = AttributeNestedSerializer(read_only=True)
    conditions = ConditionNestedSerializer(many=True, read_only=True)
    optionsets = OptionSetNestedSerializer(read_only=True, many=True)
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'locked',
            'text',
            'attribute',
            'conditions',
            'optionsets',
            'is_collection',
            'is_optional',
            'warning',
            'xml_url'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'text')

    def get_xml_url(self, obj):
        return reverse('v1-questions:question-detail-export', args=[obj.pk])


class QuestionSetNestedSerializer(serializers.ModelSerializer):

    questionsets = serializers.SerializerMethodField()
    questions = QuestionNestedSerializer(many=True, read_only=True)
    warning = serializers.SerializerMethodField()
    attribute = AttributeNestedSerializer(read_only=True)
    conditions = ConditionNestedSerializer(many=True, read_only=True)
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'locked',
            'title',
            'attribute',
            'conditions',
            'is_collection',
            'questionsets',
            'questions',
            'warning',
            'xml_url'
        )

    def get_questionsets(self, obj):
        queryset = obj.questionsets.all()
        serializer = QuestionSetNestedSerializer(queryset, many=True)
        return serializer.data

    def get_warning(self, obj):
        return get_language_warning(obj, 'title')

    def get_xml_url(self, obj):
        return reverse('v1-questions:questionset-detail-export', args=[obj.pk])


class PageNestedSerializer(serializers.ModelSerializer):

    questionsets = QuestionSetNestedSerializer(many=True, read_only=True)
    questions = QuestionNestedSerializer(many=True, read_only=True)
    warning = serializers.SerializerMethodField()
    attribute = AttributeNestedSerializer(read_only=True)
    conditions = ConditionNestedSerializer(many=True, read_only=True)
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'locked',
            'title',
            'attribute',
            'conditions',
            'is_collection',
            'questionsets',
            'questions',
            'warning',
            'xml_url'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title')

    def get_xml_url(self, obj):
        return None  # reverse('v1-questions:questionset-detail-export', args=[obj.pk])


class SectionNestedSerializer(serializers.ModelSerializer):

    pages = PageNestedSerializer(many=True)
    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'locked',
            'title',
            'pages',
            'warning',
            'xml_url'
        )

    def get_pages(self, obj):
        return [
            PageNestedSerializer(section_page.page).data
            for section_page in obj.section_pages.all()
        ]

    def get_warning(self, obj):
        return get_language_warning(obj, 'title')

    def get_xml_url(self, obj):
        return reverse('v1-questions:section-detail-export', args=[obj.pk])


class CatalogNestedSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    elements = SectionNestedSerializer(many=True, read_only=True)
    sites = SiteSerializer(many=True, read_only=True)
    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()
    export_urls = serializers.SerializerMethodField()
    projects_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Catalog
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'locked',
            'sites',
            'title',
            'help',
            'elements',
            'warning',
            'xml_url',
            'export_urls',
            'projects_count'
        )
        trans_fields = (
            'title',
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title')

    def get_xml_url(self, obj):
        return reverse('v1-questions:catalog-detail-export', args=[obj.pk])

    def get_export_urls(self, obj):
        urls = {}
        for key, text in settings.EXPORT_FORMATS:
            urls[key] = reverse('questions_catalog_export', args=[obj.pk, key])
        return urls

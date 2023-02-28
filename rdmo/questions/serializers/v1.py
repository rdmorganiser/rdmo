from django.conf import settings
from rest_framework import serializers
from rest_framework.reverse import reverse

from rdmo.conditions.models import Condition
from rdmo.core.serializers import SiteSerializer, TranslationSerializerMixin
from rdmo.core.utils import get_language_warning
from rdmo.domain.models import Attribute
from rdmo.options.models import OptionSet

from ..models import Catalog, Page, Question, QuestionSet, Section
from ..utils import get_widget_type_choices
from ..validators import (CatalogLockedValidator, CatalogUniqueURIValidator,
                          PageLockedValidator, PageUniqueURIValidator,
                          QuestionLockedValidator, QuestionSetLockedValidator,
                          QuestionSetQuestionSetValidator,
                          QuestionSetUniqueURIValidator,
                          QuestionUniqueURIValidator, SectionLockedValidator,
                          SectionUniqueURIValidator)


class CatalogSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    uri_path = serializers.CharField(required=True)
    projects_count = serializers.IntegerField(read_only=True)

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
            'sites',
            'groups',
            'projects_count'
        )
        trans_fields = (
            'title',
            'help'
        )
        validators = (
            CatalogUniqueURIValidator(),
            CatalogLockedValidator()
        )


class SectionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    uri_path = serializers.CharField(required=True)

    class Meta:
        model = Section
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'catalog',
            'order',
        )
        trans_fields = (
            'title',
        )
        validators = (
            SectionUniqueURIValidator(),
            SectionLockedValidator()
        )


class PageSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    uri_path = serializers.CharField(required=True)

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
            'section',
            'is_collection',
            'order',
            'conditions',
        )
        trans_fields = (
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
        )
        validators = (
            PageUniqueURIValidator(),
            PageLockedValidator()
        )


class QuestionSetSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    key = serializers.SlugField(required=True)

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'locked',
            'attribute',
            'page',
            'questionset',
            'is_collection',
            'order',
            'conditions',
        )
        trans_fields = (
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
        )
        validators = (
            QuestionSetUniqueURIValidator(),
            QuestionSetQuestionSetValidator(),
            QuestionSetLockedValidator()
        )


class QuestionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    key = serializers.SlugField(required=True)
    widget_type = serializers.ChoiceField(choices=get_widget_type_choices(), required=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'locked',
            'attribute',
            'page',
            'questionset',
            'is_collection',
            'is_optional',
            'order',
            'maximum',
            'minimum',
            'step',
            'default_option',
            'default_external_id',
            'widget_type',
            'value_type',
            'unit',
            'width',
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
            'sites'
        )


class SectionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'title',
            'uri'
        )


class PageIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = (
            'id',
            'title',
            'uri'
        )


class QuestionSetIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'title',
            'uri',
            'path',
        )


class QuestionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'text',
            'uri',
            'path'
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
            'path',
            'locked',
            'order',
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
            'path',
            'locked',
            'order',
            'title',
            'attribute',
            'conditions',
            'is_collection',
            'questionset',
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
            'order',
            'title',
            'attribute',
            'conditions',
            'is_collection',
            'section',
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
            'order',
            'title',
            'pages',
            'warning',
            'xml_url'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title')

    def get_xml_url(self, obj):
        return reverse('v1-questions:section-detail-export', args=[obj.pk])


class CatalogNestedSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    sections = SectionNestedSerializer(many=True, read_only=True)
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
            'order',
            'sites',
            'title',
            'help',
            'sections',
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

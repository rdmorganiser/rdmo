from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   ThroughModelSerializerMixin,
                                   TranslationSerializerMixin)

from ...models import Page, PageQuestion, PageQuestionSet, QuestionSet, Section
from ...validators import PageLockedValidator, PageUniqueURIValidator
from .question import QuestionListSerializer
from .questionset import QuestionSetNestedSerializer


class BasePageSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

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
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural'
        )
        trans_fields = (
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural'
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


class PageSerializer(ThroughModelSerializerMixin, BasePageSerializer):

    uri_path = serializers.CharField(required=True)
    sections = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all(), required=False, many=True)
    questionsets = PageQuestionSetSerializer(source='page_questionsets', read_only=False, required=False, many=True)
    questions = PageQuestionSerializer(source='page_questions', read_only=False, required=False, many=True)

    class Meta(BasePageSerializer.Meta):
        fields = BasePageSerializer.Meta.fields + (
            'sections',
            'questionsets',
            'questions',
            'conditions'
        )
        validators = (
            PageUniqueURIValidator(),
            PageLockedValidator()
        )
        parent_fields = (
            ('sections', 'section', 'page', 'section_pages'),
        )
        through_fields = (
            ('questionsets', 'page', 'questionset', 'page_questionsets'),
            ('questions', 'page', 'question', 'page_questions')
        )


class PageListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                         BasePageSerializer):

    attribute_uri = serializers.CharField(source='attribute.uri', read_only=True)
    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(BasePageSerializer.Meta):
        fields = BasePageSerializer.Meta.fields + (
            'attribute_uri',
            'warning',
            'xml_url'
        )
        warning_fields = (
            'title',
        )


class PageNestedSerializer(PageListSerializer):

    elements = serializers.SerializerMethodField()

    class Meta(PageListSerializer.Meta):
        fields = PageListSerializer.Meta.fields + (
            'elements',
        )

    def get_elements(self, obj):
        for element in obj.elements:
            if isinstance(element, QuestionSet):
                yield QuestionSetNestedSerializer(element, context=self.context).data
            else:
                yield QuestionListSerializer(element, context=self.context).data


class PageIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = (
            'id',
            'uri'
        )

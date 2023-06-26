from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementModelSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   ThroughModelSerializerMixin,
                                   TranslationSerializerMixin,
                                   ReadOnlyObjectPermissionsSerializerMixin)

from ...models import Page, PageQuestion, PageQuestionSet, QuestionSet, Section
from ...validators import PageLockedValidator, PageUniqueURIValidator
from .question import QuestionListSerializer
from .questionset import QuestionSetNestedSerializer


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


class PageSerializer(ThroughModelSerializerMixin, TranslationSerializerMixin,
                     ElementModelSerializerMixin, ReadOnlyObjectPermissionsSerializerMixin,
                     serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    uri_path = serializers.CharField(required=True)
    sections = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all(), required=False, many=True)
    questionsets = PageQuestionSetSerializer(source='page_questionsets', read_only=False, required=False, many=True)
    questions = PageQuestionSerializer(source='page_questions', read_only=False, required=False, many=True)
    read_only = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = (
            'id',
            'model',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'read_only',
            'attribute',
            'is_collection',
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
            'sections',
            'questionsets',
            'questions',
            'conditions'
        )
        trans_fields = (
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural'
        )
        parent_fields = (
            ('sections', 'section', 'page', 'section_pages'),
        )
        through_fields = (
            ('questionsets', 'page', 'questionset', 'page_questionsets'),
            ('questions', 'page', 'question', 'page_questions')
        )
        validators = (
            PageUniqueURIValidator(),
            PageLockedValidator()
        )


class PageListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                         PageSerializer):

    attribute_uri = serializers.CharField(source='attribute.uri', read_only=True)
    condition_uris = serializers.SerializerMethodField()
    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(PageSerializer.Meta):
        fields = PageSerializer.Meta.fields + (
            'attribute_uri',
            'condition_uris',
            'warning',
            'xml_url'
        )
        warning_fields = (
            'title',
        )

    def get_condition_uris(self, obj):
        return [condition.uri for condition in obj.conditions.all()]


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

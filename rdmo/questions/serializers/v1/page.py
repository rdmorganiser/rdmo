from rest_framework import serializers

from rdmo.core.serializers import (
    ElementModelSerializerMixin,
    ElementWarningSerializerMixin,
    ReadOnlyObjectPermissionSerializerMixin,
    ThroughModelSerializerMixin,
    TranslationSerializerMixin,
)

from ...models import Page, PageQuestion, PageQuestionSet, QuestionSet, Section
from ...validators import PageLockedValidator, PageUniqueURIValidator
from .question import QuestionSerializer
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
                     ElementModelSerializerMixin, ElementWarningSerializerMixin,
                     ReadOnlyObjectPermissionSerializerMixin, serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    uri_path = serializers.CharField(required=True)

    sections = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all(), required=False, many=True)
    questionsets = PageQuestionSetSerializer(source='page_questionsets', read_only=False, required=False, many=True)
    questions = PageQuestionSerializer(source='page_questions', read_only=False, required=False, many=True)

    warning = serializers.SerializerMethodField()
    read_only = serializers.SerializerMethodField()

    attribute_uri = serializers.CharField(source='attribute.uri', read_only=True)
    condition_uris = serializers.SerializerMethodField()

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
            'attribute',
            'is_collection',
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
            'sections',
            'questionsets',
            'questions',
            'conditions',
            'editors',
            'warning',
            'read_only',
            'attribute_uri',
            'condition_uris'
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
        warning_fields = (
            'title',
        )

    def get_condition_uris(self, obj):
        return [condition.uri for condition in obj.conditions.all()]


class PageNestedSerializer(PageSerializer):

    elements = serializers.SerializerMethodField()

    class Meta(PageSerializer.Meta):
        fields = (
            *PageSerializer.Meta.fields,
            'elements'
        )

    def get_elements(self, obj):
        for element in obj.elements:
            if isinstance(element, QuestionSet):
                yield QuestionSetNestedSerializer(element, context=self.context).data
            else:
                yield QuestionSerializer(element, context=self.context).data


class PageIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = (
            'id',
            'uri'
        )

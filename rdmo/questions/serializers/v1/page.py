from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   ThroughModelListField,
                                   ThroughModelSerializerMixin,
                                   TranslationSerializerMixin)

from ...models import Page, PageQuestion, PageQuestionSet, QuestionSet
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
        )


class PageQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PageQuestion
        fields = (
            'question',
        )


class PageSerializer(ThroughModelSerializerMixin, BasePageSerializer):

    uri_path = serializers.CharField(required=True)
    sections = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    questionsets = ThroughModelListField(source='page_questionsets', child=PageQuestionSetSerializer(), required=False)
    questions = ThroughModelListField(source='page_questions', child=PageQuestionSerializer(), required=False)

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


class PageListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                         BasePageSerializer):

    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(BasePageSerializer.Meta):
        fields = BasePageSerializer.Meta.fields + (
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

from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   ThroughModelSerializerMixin,
                                   TranslationSerializerMixin)

from ...models import QuestionSet, QuestionSetQuestion, QuestionSetQuestionSet
from ...validators import (QuestionSetLockedValidator,
                           QuestionSetQuestionSetValidator,
                           QuestionSetUniqueURIValidator)
from .question import QuestionListSerializer


class BaseQuestionSetSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

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


class QuestionSetSerializer(ThroughModelSerializerMixin, BaseQuestionSetSerializer):

    uri_path = serializers.CharField(required=True)
    pages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    parents = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    questionsets = QuestionSetQuestionSetSerializer(source='questionset_questionsets', read_only=False, required=False, many=True)
    questions = QuestionSetQuestionSerializer(source='questionset_questions', read_only=False, required=False, many=True)

    class Meta(BaseQuestionSetSerializer.Meta):
        fields = BaseQuestionSetSerializer.Meta.fields + (
            'pages',
            'parents',
            'questionsets',
            'questions',
            'conditions'
        )
        validators = (
            QuestionSetUniqueURIValidator(),
            QuestionSetQuestionSetValidator(),
            QuestionSetLockedValidator()
        )
        through_fields = (
            'questionsets',
            'questions'
        )


class QuestionSetListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                                BaseQuestionSetSerializer):

    attribute_uri = serializers.CharField(source='attribute.uri', read_only=True)
    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(BaseQuestionSetSerializer.Meta):
        fields = BaseQuestionSetSerializer.Meta.fields + (
            'attribute_uri',
            'warning',
            'xml_url'
        )
        warning_fields = (
            'title',
        )


class QuestionSetNestedSerializer(QuestionSetListSerializer):

    elements = serializers.SerializerMethodField()

    class Meta(QuestionSetListSerializer.Meta):
        fields = QuestionSetListSerializer.Meta.fields + (
            'elements',
        )

    def get_elements(self, obj):
        for element in obj.elements:
            if isinstance(element, QuestionSet):
                yield QuestionSetNestedSerializer(element, context=self.context).data
            else:
                yield QuestionListSerializer(element, context=self.context).data


class QuestionSetIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'uri'
        )

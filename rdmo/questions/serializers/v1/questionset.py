from rest_framework import serializers

from rdmo.core.serializers import (
    ElementModelSerializerMixin,
    ElementWarningSerializerMixin,
    ReadOnlyObjectPermissionSerializerMixin,
    ThroughModelSerializerMixin,
    TranslationSerializerMixin,
)

from ...models import Page, QuestionSet, QuestionSetQuestion, QuestionSetQuestionSet
from ...validators import QuestionSetLockedValidator, QuestionSetQuestionSetValidator, QuestionSetUniqueURIValidator
from .question import QuestionSerializer


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


class QuestionSetSerializer(ThroughModelSerializerMixin, TranslationSerializerMixin,
                            ElementModelSerializerMixin, ElementWarningSerializerMixin,
                            ReadOnlyObjectPermissionSerializerMixin, serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    uri_path = serializers.CharField(required=True)

    pages = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all(), required=False, many=True)
    parents = serializers.PrimaryKeyRelatedField(queryset=QuestionSet.objects.all(), required=False, many=True)
    questionsets = QuestionSetQuestionSetSerializer(source='questionset_questionsets',
                                                    read_only=False, required=False, many=True)
    questions = QuestionSetQuestionSerializer(source='questionset_questions',
                                              read_only=False, required=False, many=True)

    warning = serializers.SerializerMethodField()
    read_only = serializers.SerializerMethodField()

    attribute_uri = serializers.CharField(source='attribute.uri', read_only=True)
    condition_uris = serializers.SerializerMethodField()

    class Meta:
        model = QuestionSet
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
            'pages',
            'parents',
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
            ('pages', 'page', 'questionset', 'page_questionsets'),
            ('parents', 'parent', 'questionset', 'questionset_questionsets')
        )
        through_fields = (
            ('questionsets', 'parent', 'questionset', 'questionset_questionsets'),
            ('questions', 'questionset', 'question', 'questionset_questions')
        )
        validators = (
            QuestionSetUniqueURIValidator(),
            QuestionSetQuestionSetValidator(),
            QuestionSetLockedValidator()
        )
        warning_fields = (
            'title',
        )

    def get_condition_uris(self, obj):
        return [condition.uri for condition in obj.conditions.all()]


class QuestionSetNestedSerializer(QuestionSetSerializer):

    elements = serializers.SerializerMethodField()

    class Meta(QuestionSetSerializer.Meta):
        fields = (
            *QuestionSetSerializer.Meta.fields,
            'elements'
        )

    def get_elements(self, obj):
        for element in obj.elements:
            if isinstance(element, QuestionSet):
                yield QuestionSetNestedSerializer(element, context=self.context).data
            else:
                yield QuestionSerializer(element, context=self.context).data


class QuestionSetIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'uri'
        )

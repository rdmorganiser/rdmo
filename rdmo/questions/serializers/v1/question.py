from rest_framework import serializers

from rdmo.core.serializers import (ElementModelSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   ReadOnlyObjectPermissionSerializerMixin,
                                   ThroughModelSerializerMixin,
                                   TranslationSerializerMixin)

from ...models import Page, Question, QuestionSet
from ...validators import QuestionLockedValidator, QuestionUniqueURIValidator


class QuestionSerializer(ThroughModelSerializerMixin, TranslationSerializerMixin,
                         ElementModelSerializerMixin, ElementWarningSerializerMixin,
                         ReadOnlyObjectPermissionSerializerMixin, serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    uri_path = serializers.CharField(required=True)

    pages = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all(), required=False, many=True)
    questionsets = serializers.PrimaryKeyRelatedField(queryset=QuestionSet.objects.all(), required=False, many=True)

    warning = serializers.SerializerMethodField()
    read_only = serializers.SerializerMethodField()

    attribute_uri = serializers.CharField(source='attribute.uri', read_only=True)
    condition_uris = serializers.SerializerMethodField()
    optionset_uris = serializers.SerializerMethodField()

    class Meta:
        model = Question
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
            'text',
            'help',
            'default_text',
            'verbose_name',
            'verbose_name_plural',
            'pages',
            'questionsets',
            'optionsets',
            'conditions',
            'editors',
            'warning',
            'read_only',
            'attribute_uri',
            'condition_uris',
            'optionset_uris'
        )
        trans_fields = (
            'text',
            'help',
            'default_text',
            'verbose_name',
            'verbose_name_plural',
        )
        parent_fields = (
            ('pages', 'page', 'question', 'page_questions'),
            ('questionsets', 'questionset', 'question', 'questionset_questions')
        )
        validators = (
            QuestionUniqueURIValidator(),
            QuestionLockedValidator()
        )
        warning_fields = (
            'text',
        )

    def to_internal_value(self, data):
        # handles an empty width, maximum, minimum, or step field
        for field in ['width', 'maximum', 'minimum', 'step']:
            if data.get(field) == '':
                data[field] = None

        return super().to_internal_value(data)

    def get_condition_uris(self, obj):
        return [condition.uri for condition in obj.conditions.all()]

    def get_optionset_uris(self, obj):
        return [optionset.uri for optionset in obj.optionsets.all()]


class QuestionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'uri'
        )

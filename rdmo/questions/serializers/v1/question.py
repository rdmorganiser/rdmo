from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementModelSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   ThroughModelSerializerMixin,
                                   TranslationSerializerMixin,
                                   ReadOnlyObjectPermissionsSerializerMixin)

from ...models import Page, Question, QuestionSet
from ...validators import QuestionLockedValidator, QuestionUniqueURIValidator


class QuestionSerializer(ThroughModelSerializerMixin, TranslationSerializerMixin,
                         ElementModelSerializerMixin, ReadOnlyObjectPermissionsSerializerMixin,
                         serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    uri_path = serializers.CharField(required=True)
    pages = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all(), required=False, many=True)
    questionsets = serializers.PrimaryKeyRelatedField(queryset=QuestionSet.objects.all(), required=False, many=True)
    read_only = serializers.SerializerMethodField()

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
            'read_only',
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
            'conditions'
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

    def to_internal_value(self, data):
        # handles an empty width, maximum, minimum, or step field
        for field in ['width', 'maximum', 'minimum', 'step']:
            if data.get(field) == '':
                data[field] = None

        return super().to_internal_value(data)


class QuestionListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                             QuestionSerializer):

    attribute_uri = serializers.CharField(source='attribute.uri', read_only=True)
    condition_uris = serializers.SerializerMethodField()
    optionset_uris = serializers.SerializerMethodField()
    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(QuestionSerializer.Meta):
        fields = QuestionSerializer.Meta.fields + (
            'attribute_uri',
            'condition_uris',
            'optionset_uris',
            'warning',
            'xml_url'
        )
        warning_fields = (
            'text',
        )

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

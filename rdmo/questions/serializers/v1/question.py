from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   ThroughModelSerializerMixin,
                                   TranslationSerializerMixin)

from ...models import Question
from ...validators import QuestionLockedValidator, QuestionUniqueURIValidator


class BaseQuestionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

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
            'text',
            'help',
            'default_text',
            'verbose_name',
            'verbose_name_plural'
        )
        trans_fields = (
            'text',
            'help',
            'default_text',
            'verbose_name',
            'verbose_name_plural',
        )


class QuestionSerializer(ThroughModelSerializerMixin, BaseQuestionSerializer):

    uri_path = serializers.CharField(required=True)
    pages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    questionsets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta(BaseQuestionSerializer.Meta):
        fields = BaseQuestionSerializer.Meta.fields + (
            'pages',
            'questionsets',
            'optionsets',
            'conditions'
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
                             BaseQuestionSerializer):

    attribute_uri = serializers.CharField(source='attribute.uri', read_only=True)
    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(BaseQuestionSerializer.Meta):
        fields = BaseQuestionSerializer.Meta.fields + (
            'attribute_uri',
            'warning',
            'xml_url'
        )
        warning_fields = (
            'text',
        )


class QuestionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'uri'
        )

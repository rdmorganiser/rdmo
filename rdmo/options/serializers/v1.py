from rest_framework import serializers
from rest_framework.reverse import reverse

from rdmo.conditions.models import Condition
from rdmo.core.serializers import (ThroughModelSerializerMixin,
                                   TranslationSerializerMixin)
from rdmo.core.utils import get_language_warning
from rdmo.questions.models import QuestionSet

from ..models import Option, OptionSet, OptionSetOption
from ..validators import (OptionLockedValidator, OptionSetLockedValidator,
                          OptionSetUniqueURIValidator,
                          OptionUniqueURIValidator)


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'uri'
        )


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'uri'
        )


class OptionSetOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSetOption
        fields = (
            'option',
            'order'
        )


class OptionSetSerializer(ThroughModelSerializerMixin, serializers.ModelSerializer):

    uri_path = serializers.CharField(required=True)

    options = OptionSetOptionSerializer(source='optionset_options', read_only=False, required=False, many=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'order',
            'provider_key',
            'options',
            'conditions',
            'questions'
        )
        through_fields = (
            'optionset_options',
        )
        validators = (
            OptionSetUniqueURIValidator(),
            OptionSetLockedValidator()
        )


class OptionOptionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSetOption
        fields = (
            'optionset',
            'order'
        )


class OptionSerializer(ThroughModelSerializerMixin, TranslationSerializerMixin, serializers.ModelSerializer):

    uri_path = serializers.CharField(required=True)
    optionsets = OptionOptionSetSerializer(source='option_optionsets', read_only=False, required=False, many=True)
    values_count = serializers.IntegerField(read_only=True)
    projects_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Option
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'text',
            'label',
            'additional_input',
            'optionsets',
            'values_count',
            'projects_count'
        )
        trans_fields = (
            'text',
        )
        through_fields = (
            'option_optionsets',
        )
        validators = (
            OptionUniqueURIValidator(),
            OptionLockedValidator()
        )


class OptionSetIndexOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'uri'
        )


class OptionSetIndexSerializer(serializers.ModelSerializer):

    options = OptionSetIndexOptionSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri',
            'options'
        )


class OptionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'optionsets',
            'uri',
            'text'
        )


class ConditionNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'uri'
        )


class ProviderNestedSerializer(serializers.Serializer):

    key = serializers.CharField()
    label = serializers.CharField()
    class_name = serializers.CharField()

    class Meta:
        fields = (
            'key',
            'label',
            'class_name'
        )


class OptionNestedSerializer(serializers.ModelSerializer):

    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'locked',
            'text',
            'warning',
            'xml_url'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'text')

    def get_xml_url(self, obj):
        return reverse('v1-options:option-detail-export', args=[obj.pk])


class OptionSetNestedSerializer(serializers.ModelSerializer):

    options = OptionNestedSerializer(many=True)
    conditions = ConditionNestedSerializer(many=True)
    provider = ProviderNestedSerializer()
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'order',
            'locked',
            'provider',
            'options',
            'conditions',
            'xml_url'
        )

    def get_xml_url(self, obj):
        return reverse('v1-options:optionset-detail-export', args=[obj.pk])

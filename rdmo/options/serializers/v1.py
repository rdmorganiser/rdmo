from rest_framework import serializers
from rest_framework.reverse import reverse

from rdmo.conditions.models import Condition
from rdmo.core.serializers import TranslationSerializerMixin
from rdmo.core.utils import get_language_warning
from rdmo.questions.models import QuestionSet

from ..models import Option, OptionSet
from ..validators import OptionSetUniqueKeyValidator, OptionUniquePathValidator


class QuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'key'
        )


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'key'
        )


class OptionSetSerializer(serializers.ModelSerializer):

    questionsets = QuestionSetSerializer(many=True, read_only=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'provider_key',
            'conditions',
            'questionsets'
        )
        validators = (OptionSetUniqueKeyValidator(), )


class OptionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    optionset = serializers.PrimaryKeyRelatedField(queryset=OptionSet.objects.all(), required=True)

    conditions = ConditionSerializer(many=True, read_only=True)

    class Meta:
        model = Option
        fields = (
            'id',
            'optionset',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'text',
            'label',
            'additional_input',
            'conditions'
        )
        trans_fields = (
            'text',
        )
        validators = (OptionUniquePathValidator(), )


class OptionSetIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'key',
        )


class OptionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'optionset',
            'key',
            'text'
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
            'uri_prefix',
            'path',
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
    provider = ProviderNestedSerializer()
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri_prefix',
            'key',
            'provider',
            'options',
            'xml_url'
        )

    def get_xml_url(self, obj):
        return reverse('v1-options:optionset-detail-export', args=[obj.pk])

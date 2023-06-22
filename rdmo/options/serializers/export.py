from rest_framework import serializers

from rdmo.conditions.serializers.export import ConditionExportSerializer
from rdmo.core.serializers import TranslationSerializerMixin

from ..models import Option, OptionSet, OptionSetOption


class OptionExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'additional_input'
        )
        trans_fields = (
            'text',
        )


class OptionSetOptionExportSerializer(serializers.ModelSerializer):

    option = OptionExportSerializer()

    class Meta:
        model = OptionSetOption
        fields = (
            'option',
            'order'
        )


class OptionSetExportSerializer(serializers.ModelSerializer):

    optionset_options = OptionSetOptionExportSerializer(many=True)
    conditions = ConditionExportSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'order',
            'provider_key',
            'optionset_options',
            'conditions'
        )

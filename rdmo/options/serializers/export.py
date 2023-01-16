from rdmo.core.serializers import TranslationSerializerMixin
from rest_framework import serializers

from ..models import Option, OptionSet


class OptionExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    optionsets = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'order',
            'additional_input',
            'optionsets'
        )
        trans_fields = (
            'text',
        )

    def get_optionsets(self, obj):
        return [optionset.uri for optionset in obj.optionsets.all()]


class OptionSetExportSerializer(serializers.ModelSerializer):

    options = OptionExportSerializer(many=True)
    conditions = serializers.SerializerMethodField()

    class Meta:
        model = OptionSet
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'order',
            'provider_key',
            'options',
            'conditions'
        )

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]

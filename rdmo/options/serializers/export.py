from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin

from ..models import OptionSet, Option


class OptionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    optionset = serializers.CharField(source='optionset.uri', default=None, read_only=True)

    class Meta:
        model = Option
        fields = (
            'uri',
            'uri_prefix',
            'key',
            'path',
            'comment',
            'order',
            'additional_input',
            'optionset'
        )
        trans_fields = (
            'text',
        )


class OptionSetSerializer(serializers.ModelSerializer):

    options = OptionSerializer(many=True)
    conditions = serializers.SerializerMethodField()

    class Meta:
        model = OptionSet
        fields = (
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'options',
            'conditions'
        )

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]

from rest_framework import serializers

from ..models import OptionSet, Option


class OptionSerializer(serializers.ModelSerializer):

    optionset = serializers.CharField(source='optionset.uri', default=None, read_only=True)

    class Meta:
        model = Option
        fields = (
            'uri',
            'comment',
            'order',
            'text_en',
            'text_de',
            'additional_input',
            'optionset'
        )


class OptionSetSerializer(serializers.ModelSerializer):

    options = OptionSerializer(many=True)
    conditions = serializers.SerializerMethodField()

    class Meta:
        model = OptionSet
        fields = (
            'uri',
            'comment',
            'order',
            'options',
            'conditions'
        )

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]

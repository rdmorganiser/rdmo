from rest_framework import serializers

from rdmo.conditions.models import Condition

from ..models import OptionSet, Option


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'uri',
            'comment',
            'order',
            'text_en',
            'text_de',
            'additional_input'
        )


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'uri',
        )


class OptionSetSerializer(serializers.ModelSerializer):

    options = OptionSerializer(many=True)
    conditions = ConditionSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'uri',
            'comment',
            'order',
            'options',
            'conditions'
        )

from rest_framework import serializers

from .models import *

from apps.domain.models import Attribute
from apps.conditions.models import Condition


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'full_title',
            'value_type'
        )


class ConditionSerializer(serializers.ModelSerializer):

    source = AttributeSerializer()

    class Meta:
        model = Condition
        fields = (
            'source',
            'relation',
            'target',
        )


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            '__str__',
            'attribute',
            'time_period',
            'title_en',
            'title_de',
            'text_en',
            'text_de'
        )


class TaskIndexSerializer(serializers.ModelSerializer):

    attribute = AttributeSerializer()
    conditions = ConditionSerializer(many=True)

    class Meta:
        model = Task
        fields = (
            'id',
            '__str__',
            'attribute',
            'time_period',
            'title',
            'text',
            'conditions'
        )

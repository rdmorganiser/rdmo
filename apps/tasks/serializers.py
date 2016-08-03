from rest_framework import serializers

from .models import *

from apps.domain.models import Attribute
from apps.conditions.models import Condition


class TaskIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'text'
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
            'text_de',
            'conditions'
        )


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'label',
            'value_type'
        )


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'label'
        )

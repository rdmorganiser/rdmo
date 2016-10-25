from rest_framework import serializers

from apps.domain.models import Attribute
from apps.options.models import Option

from .models import *


class ConditionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'title',
            'description',
            'source_label',
            'relation_label',
            'target_label'
        )


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'title',
            'description',
            'source',
            'relation',
            'target_text',
            'target_option'
        )


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'label'
        )


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'order',
            'text'
        )

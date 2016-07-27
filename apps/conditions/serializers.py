from rest_framework import serializers

from apps.domain.models import Attribute, Option

from .models import *


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            '__str__',
            'source',
            'relation',
            'target_text',
            'target_option'
        )


class ConditionIndexSerializer(serializers.ModelSerializer):

    source = serializers.CharField(source='source.full_title')

    class Meta:
        model = Condition
        fields = (
            'id',
            '__str__',
            'source',
            'relation_str',
            'target_str'
        )


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'full_title'
        )


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'attribute',
            'order',
            'text'
        )

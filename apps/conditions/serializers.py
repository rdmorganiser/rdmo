from rest_framework import serializers

from apps.domain.models import Attribute

from .models import *


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'full_title'
        )


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
            'relation',
            'target'
        )

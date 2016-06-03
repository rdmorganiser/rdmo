from rest_framework import serializers

from apps.core.serializers import RecursiveField

from .models import *


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = ('id', 'attribute', 'order', 'text', 'text_en', 'text_de', 'additional_input')


class RangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Range
        fields = ('id', 'minimum', 'maximum', 'step')


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = ('id', 'attribute', 'source_attribute', 'relation', 'target_text', 'target_option')


class AttributeEntitySerializer(serializers.ModelSerializer):

    children = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = ('id', 'title', 'is_collection', 'children')


class AttributeSerializer(serializers.ModelSerializer):

    full_title = serializers.ReadOnlyField()
    options = OptionSerializer(many=True, read_only=True)
    range = RangeSerializer(read_only=True)
    conditions = ConditionSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = ('id', 'title', 'full_title', 'is_collection', 'value_type', 'unit', 'parent_entity', 'conditions', 'range', 'options')

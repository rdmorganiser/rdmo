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
        fields = ('id', 'attribute', 'minimum', 'maximum', 'step')


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = ('id', 'attribute', 'source_attribute', 'relation', 'target_text', 'target_option')


class NestedRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Range
        fields = ('id', )


class NestedAttributeEntitySerializer(serializers.ModelSerializer):

    children = RecursiveField(many=True, read_only=True)
    range = NestedRangeSerializer()

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'title',
            'full_title',
            'is_collection',
            'is_attribute',
            'range',
            'has_options',
            'has_conditions',
            'children'
        )


class AttributeEntitySerializer(serializers.ModelSerializer):

    full_title = serializers.ReadOnlyField()
    options = OptionSerializer(many=True, read_only=True)
    range = RangeSerializer(read_only=True)
    conditions = ConditionSerializer(many=True, read_only=True)

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'parent_entity',
            'title',
            'full_title',
            'description',
            'uri',
            'is_collection',
            'conditions',
            'range',
            'options'
        )


class AttributeSerializer(AttributeEntitySerializer):

    full_title = serializers.ReadOnlyField()
    options = OptionSerializer(many=True, read_only=True)
    range = RangeSerializer(read_only=True)
    conditions = ConditionSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = (
            'id',
            'parent_entity',
            'title',
            'full_title',
            'description',
            'uri',
            'is_collection',
            'conditions',
            'range',
            'options',
            'value_type',
            'unit'
        )

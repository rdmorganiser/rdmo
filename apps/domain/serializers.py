from rest_framework import serializers

from apps.core.serializers import RecursiveField

from .models import *


class AttributeEntitySerializer(serializers.ModelSerializer):

    full_title = serializers.ReadOnlyField()

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'parent_entity',
            'title',
            'full_title',
            'description',
            'uri',
            'is_collection'
        )


class AttributeSerializer(AttributeEntitySerializer):

    full_title = serializers.ReadOnlyField()

    class Meta:
        model = Attribute
        fields = (
            'id',
            'parent_entity',
            'title',
            'full_title',
            'description',
            'uri',
            'value_type',
            'unit',
            'is_collection'
        )


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'attribute',
            'order',
            'text',
            'text_en',
            'text_de',
            'additional_input'
        )


class RangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Range
        fields = (
            'id',
            'attribute',
            'minimum',
            'maximum',
            'step'
        )


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'attribute_entity',
            'source_attribute',
            'relation',
            'target_text',
            'target_option'
        )


class VerboseNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerboseName
        fields = (
            'id',
            'attribute_entity',
            'name_en',
            'name_de',
            'name_plural_en',
            'name_plural_de'
        )


class NestedAttributeEntitySerializer(serializers.ModelSerializer):

    class NestedRangeSerializer(serializers.ModelSerializer):

        class Meta:
            model = Range
            fields = ('id', )

    class NestedVerboseNameSerializer(serializers.ModelSerializer):

        class Meta:
            model = VerboseName
            fields = ('id', )

    children = RecursiveField(many=True, read_only=True)

    range = NestedRangeSerializer()
    verbosename = NestedVerboseNameSerializer()

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'title',
            'full_title',
            'is_collection',
            'is_attribute',
            'range',
            'verbosename',
            'has_options',
            'has_conditions',
            'children'
        )

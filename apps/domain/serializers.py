from rest_framework import serializers

from apps.conditions.models import Condition

from .models import *


class AttributeEntityNestedSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'title',
            'label',
            'is_collection',
            'is_attribute',
            'children'
        )

    def get_children(self, obj):
        # get the children from the cached mptt tree
        return AttributeEntityNestedSerializer(obj.get_children(), many=True, read_only=True).data


class AttributeEntityIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'label'
        )


class AttributeEntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'parent',
            'title',
            'description',
            'uri',
            'is_collection',
            'conditions'
        )


class AttributeIndexSerializer(AttributeEntitySerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'label'
        )


class AttributeSerializer(AttributeEntitySerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'parent',
            'title',
            'description',
            'uri',
            'value_type',
            'unit',
            'is_collection',
            'conditions'
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


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'label',
        )

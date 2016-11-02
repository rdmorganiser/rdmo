from rest_framework import serializers

from apps.options.models import OptionSet
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
            'optionsets',
            'conditions'
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


class OptionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'title',
        )


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'title',
        )


class ExportVerboseNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerboseName
        fields = (
            'name_en',
            'name_de',
            'name_plural_en',
            'name_plural_de'
        )


class ExportRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Range
        fields = (
            'minimum',
            'maximum',
            'step'
        )


class ExportConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'source',
            'relation',
            'target_text',
            'target_option'
        )


class ExportSerializer(serializers.ModelSerializer):

    value_type = serializers.CharField(source='attribute.value_type', read_only=True)
    unit = serializers.CharField(source='attribute.unit', read_only=True)

    # options = ExportOptionSerializer(source='attribute.options', many=True, read_only=True)
    range = ExportRangeSerializer(source='attribute.range', read_only=True)
    verbosename = ExportVerboseNameSerializer(read_only=True)
    conditions = ExportConditionSerializer(many=True, read_only=True)

    children = serializers.SerializerMethodField()

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'title',
            'description',
            'uri',
            'is_collection',
            'is_attribute',
            'value_type',
            'unit',
            'is_collection',
            'conditions',
            # 'options',
            'range',
            'verbosename',
            'conditions',
            'children'
        )

    def get_children(self, obj):
        # get the children from the cached mptt tree
        return ExportSerializer(obj.get_children(), many=True, read_only=True).data

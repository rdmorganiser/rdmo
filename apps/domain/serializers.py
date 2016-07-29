from rest_framework import serializers

from apps.core.serializers import RecursiveField

from apps.conditions.models import Condition

from .models import *


class AttributeEntityNestedSerializer(serializers.ModelSerializer):

    children = RecursiveField(many=True, read_only=True)

    range = serializers.SerializerMethodField()
    verbosename = serializers.SerializerMethodField()

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

    def get_range(self, obj):
        return {'id': obj.range.pk} if hasattr(obj, 'range') and obj.range else None

    def get_verbosename(self, obj):
        return {'id': obj.verbosename.pk} if hasattr(obj, 'verbosename') and obj.verbosename else None


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
            'is_collection',
            'conditions'
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
            '__str__'
        )


class ExportOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'order',
            'text_en',
            'text_de',
            'additional_input'
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
            'source_attribute',
            'relation',
            'target_text',
            'target_option'
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


class ExportSerializer(serializers.ModelSerializer):

    value_type = serializers.CharField(source='attribute.value_type', read_only=True)
    unit = serializers.CharField(source='attribute.unit', read_only=True)

    options = ExportOptionSerializer(source='attribute.options', many=True, read_only=True)
    range = ExportRangeSerializer(source='attribute.range', read_only=True)
    verbosename = ExportVerboseNameSerializer(read_only=True)
    conditions = ExportConditionSerializer(many=True, read_only=True)

    children = RecursiveField(many=True, read_only=True)

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
            'conditions'
        )

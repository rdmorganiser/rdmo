from rest_framework import serializers

from apps.core.serializers import RecursiveField

from apps.conditions.models import Condition

from .models import *


class AttributeEntityNestedSerializer(serializers.ModelSerializer):

    # children = RecursiveField(many=True, read_only=True)

    # range = serializers.SerializerMethodField()
    # verbosename = serializers.SerializerMethodField()

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'title',
            'full_title',
            'is_collection',
            'is_attribute',
            # 'range',
            # 'verbosename',
            'has_options',
            'has_conditions',
            # 'children'
        )

    # def get_range(self, obj):
    #     return {'id': obj.range.pk} if hasattr(obj, 'range') and obj.range else None

    # def get_verbosename(self, obj):
    #     return {'id': obj.verbosename.pk} if hasattr(obj, 'verbosename') and obj.verbosename else None


class AttributeEntitySerializer(serializers.ModelSerializer):

    full_title = serializers.ReadOnlyField()

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'parent',
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
            'parent',
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

from django.utils.translation import ugettext_lazy as _

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
        fields = ('id', 'attribute_entity', 'source_attribute', 'relation', 'target_text', 'target_option')


class VerboseNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerboseName
        fields = ('id', 'attribute_entity', 'name_en', 'name_de', 'name_plural_en', 'name_plural_de')


class NestedRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Range
        fields = ('id', )


class NestedVerboseNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerboseName
        fields = ('id', )


class NestedAttributeEntitySerializer(serializers.ModelSerializer):

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


class AttributeEntityVerboseNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerboseName
        fields = ('name', 'name_plural')


class AttributeEntitySerializer(serializers.ModelSerializer):

    full_title = serializers.ReadOnlyField()
    options = OptionSerializer(many=True, read_only=True)
    range = RangeSerializer(read_only=True)
    verbosename = VerboseNameSerializer(read_only=True)
    conditions = ConditionSerializer(many=True, read_only=True)

    verbosename = serializers.SerializerMethodField()

    id_attribute = serializers.SerializerMethodField()

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
            'verbosename',
            'options',
            'id_attribute'
        )

    def get_verbosename(self, obj):
        try:
            return AttributeEntityVerboseNameSerializer(instance=obj.verbosename).data
        except VerboseName.DoesNotExist:
            return {
                'name': _('set'),
                'name_plural': _('sets')
            }

    def get_id_attribute(self, obj):
        try:
            attribute = obj.children.get(title='id')
            return {'id': attribute.pk}
        except AttributeEntity.DoesNotExist:
            return None


class AttributeSerializer(AttributeEntitySerializer):

    full_title = serializers.ReadOnlyField()
    options = OptionSerializer(many=True, read_only=True)
    range = RangeSerializer(read_only=True)
    conditions = ConditionSerializer(many=True, read_only=True)

    verbosename = serializers.SerializerMethodField()

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
            'verbosename',
            'options',
            'value_type',
            'unit'
        )

    def get_verbosename(self, obj):
        try:
            return AttributeEntityVerboseNameSerializer(instance=obj.verbosename).data
        except VerboseName.DoesNotExist:
            return {
                'name': _('item'),
                'name_plural': _('items')
            }


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
    verbosename = ExportVerboseNameSerializer(source='attribute.verbosename', read_only=True)
    conditions = ExportConditionSerializer(source='attribute.conditions', many=True, read_only=True)

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
            'children',
            'options',
            'range',
            'verbosename',
            'conditions'
        )

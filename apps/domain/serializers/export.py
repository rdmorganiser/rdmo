from rest_framework import serializers

from ..models import AttributeEntity, Range, VerboseName


class VerboseNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerboseName
        fields = (
            'name_en',
            'name_de',
            'name_plural_en',
            'name_plural_de'
        )


class RangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Range
        fields = (
            'minimum',
            'maximum',
            'step'
        )


class AttributeEntitySerializer(serializers.ModelSerializer):

    value_type = serializers.CharField(source='attribute.value_type', read_only=True)
    unit = serializers.CharField(source='attribute.unit', read_only=True)

    range = RangeSerializer(source='attribute.range', read_only=True)
    verbosename = VerboseNameSerializer(read_only=True)

    optionsets = serializers.SerializerMethodField()
    conditions = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = AttributeEntity
        fields = (
            'uri',
            'comment',
            'is_collection',
            'is_attribute',
            'value_type',
            'unit',
            'is_collection',
            'range',
            'verbosename',
            'conditions',
            'optionsets',
            'children'
        )

    def get_children(self, obj):
        # get the children from the cached mptt tree
        return AttributeEntitySerializer(obj.get_children(), many=True, read_only=True).data

    def get_optionsets(self, obj):
        if hasattr(obj, 'attribute'):
            return [option.uri for option in obj.attribute.optionsets.all()]

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]

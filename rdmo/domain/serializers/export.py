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

    range = RangeSerializer(source='attribute.range', default=None, read_only=True)
    verbosename = VerboseNameSerializer(read_only=True)

    children = serializers.SerializerMethodField()

    class Meta:
        model = AttributeEntity
        fields = (
            'uri',
            'comment',
            'is_attribute',
            'range',
            'verbosename',
            'children'
        )

    def get_children(self, obj):
        # get the children from the cached mptt tree
        return AttributeEntitySerializer(obj.get_children(), many=True, read_only=True).data

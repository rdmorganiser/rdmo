from rest_framework import serializers

from ..models import AttributeEntity, Attribute, Range, VerboseName
from ..validators import AttributeEntityUniquePathValidator


class AttributeEntityNestedSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'path',
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
            'path'
        )


class AttributeIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'path'
        )


class AttributeEntitySerializer(serializers.ModelSerializer):

    path = serializers.CharField(read_only=True)

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'path',
            'parent',
            'uri_prefix',
            'key',
            'comment',
            'is_collection'
        )
        validators = (AttributeEntityUniquePathValidator(), )


class AttributeSerializer(serializers.ModelSerializer):

    path = serializers.CharField(read_only=True)

    class Meta:
        model = Attribute
        fields = (
            'id',
            'path',
            'parent',
            'uri_prefix',
            'key',
            'comment',
            'is_collection'
        )
        validators = (AttributeEntityUniquePathValidator(), )


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

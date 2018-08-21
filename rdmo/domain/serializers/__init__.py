from rest_framework import serializers

from ..models import Attribute
from ..validators import AttributeUniquePathValidator


class AttributeNestedSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = (
            'id',
            'path',
            'children'
        )

    def get_children(self, obj):
        # get the children from the cached mptt tree
        return AttributeNestedSerializer(obj.get_children(), many=True, read_only=True).data


class AttributeIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'path'
        )


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
        )
        validators = (AttributeUniquePathValidator(), )

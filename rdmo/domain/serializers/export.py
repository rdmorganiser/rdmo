from rest_framework import serializers

from ..models import Attribute


class AttributeSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = (
            'uri',
            'comment',
            'children'
        )

    def get_children(self, obj):
        # get the children from the cached mptt tree
        return AttributeSerializer(obj.get_children(), many=True, read_only=True).data

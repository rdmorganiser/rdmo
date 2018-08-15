from rest_framework import serializers

from ..models import AttributeEntity


class AttributeEntitySerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()

    class Meta:
        model = AttributeEntity
        fields = (
            'uri',
            'comment',
            'is_attribute',
            'children'
        )

    def get_children(self, obj):
        # get the children from the cached mptt tree
        return AttributeEntitySerializer(obj.get_children(), many=True, read_only=True).data

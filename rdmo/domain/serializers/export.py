from rest_framework import serializers

from ..models import Attribute


class AttributeExportSerializer(serializers.ModelSerializer):

    parent = serializers.CharField(source='parent.uri', default=None, read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = (
            'uri',
            'uri_prefix',
            'key',
            'path',
            'comment',
            'parent',
            'children'
        )

    def get_children(self, obj):
        # get the children from the cached mptt tree
        return AttributeExportSerializer(obj.get_children(), many=True, read_only=True).data

from rest_framework import serializers

from ..models import Attribute


class AttributeExportSerializer(serializers.ModelSerializer):

    parent = serializers.CharField(source='parent.uri', default=None, read_only=True)
    parent_data = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = (
            'uri',
            'uri_prefix',
            'key',
            'path',
            'comment',
            'parent',
            'parent_data'
        )

    def get_parent_data(self, obj):
        if obj.parent is not None:
            return AttributeExportSerializer(obj.parent).data

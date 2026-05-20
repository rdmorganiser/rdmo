from rest_framework import serializers

from ..models import Attribute


class AttributeExportSerializer(serializers.ModelSerializer):

    parent = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = (
            'uri',
            'uri_prefix',
            'key',
            'path',
            'comment',
            'parent',
        )

    def get_parent(self, obj):
        parent = self.context.get('attribute_map', {}).get(obj.parent_id)
        if parent:
            return AttributeExportSerializer(parent, context=self.context).data

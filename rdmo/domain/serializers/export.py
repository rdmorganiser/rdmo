from rest_framework import serializers

from ..models import Attribute


class AttributeExportSerializer(serializers.ModelSerializer):

    parent = serializers.SerializerMethodField()
    parent_uri = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = (
            'uri',
            'uri_prefix',
            'key',
            'path',
            'comment',
            'parent',
            'parent_uri',
        )

    def __init__(self, *args, include_parent=True, **kwargs):
        self.include_parent = include_parent
        super().__init__(*args, **kwargs)

    def get_parent(self, obj):
        if self.include_parent:
            parent = self.context.get('attribute_map', {}).get(obj.parent_id)
            if parent:
                return AttributeExportSerializer(parent, context=self.context).data

    def get_parent_uri(self, obj):
        parent = self.context.get('attribute_map', {}).get(obj.parent_id)
        if parent:
            return parent.uri

from rest_framework import serializers

from ..models import Attribute


class AttributeExportSerializer(serializers.ModelSerializer):

    parent = serializers.SerializerMethodField()
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
            'parent_data',
        )

    def get_parent(self, obj):
        parent = self.get_parent_object_from_context(obj)
        return parent.uri if parent is not None else None

    def get_parent_data(self, obj):
        parent = self.get_parent_object_from_context(obj)

        if parent is None:
            return None

        cache = self.context.setdefault('parent_data_cache', {})

        if parent.pk not in cache:
            cache[parent.pk] = AttributeExportSerializer(
                parent,
                context=self.context,
            ).data

        return cache[parent.pk]

    def get_parent_object_from_context(self, obj):
        if obj.parent_id is None:
            return None

        attributes_by_id = self.context.get('attributes_by_id', {})

        if obj.parent_id in attributes_by_id:
            return attributes_by_id[obj.parent_id]

        # fallback for edge cases, but this can query
        return obj.parent

from rest_framework import serializers

from ..models import Attribute


class AttributeExportSerializer(serializers.ModelSerializer):

    parent = serializers.CharField(source='parent.uri', default=None, read_only=True)

    class Meta:
        model = Attribute
        fields = (
            'uri',
            'uri_prefix',
            'key',
            'path',
            'comment',
            'parent'
        )

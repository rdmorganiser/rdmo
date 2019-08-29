from rest_framework import serializers

from ..models import Attribute
from ..validators import AttributeUniquePathValidator

import logging
log = logging.getLogger(__name__)


class AttributeSerializer(serializers.ModelSerializer):

    key = serializers.CharField(required=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), default=None, allow_null=True)
    path = serializers.CharField(required=False)

    class Meta:
        model = Attribute
        fields = (
            'id',
            'parent',
            'uri_prefix',
            'key',
            'path',
            'comment',
        )
        validators = (AttributeUniquePathValidator(), )


class NestedAttributeSerializer(serializers.ModelSerializer):

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
        return NestedAttributeSerializer(obj.get_children(), many=True, read_only=True).data

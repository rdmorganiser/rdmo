import logging

from rest_framework import serializers

from rdmo.core.serializers import ElementExportSerializerMixin

from ..models import Attribute
from ..validators import (AttributeLockedValidator, AttributeParentValidator,
                          AttributeUniqueURIValidator)

log = logging.getLogger(__name__)


class BaseAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'locked',
            'parent'
        )


class AttributeSerializer(BaseAttributeSerializer):

    key = serializers.SlugField(required=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), default=None, allow_null=True)
    conditions = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    questionsets = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    questions = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    tasks_as_start = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    tasks_as_end = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    tasks_as_start = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    tasks_as_start = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    projects_count = serializers.IntegerField(read_only=True)
    values_count = serializers.IntegerField(read_only=True)

    class Meta(BaseAttributeSerializer.Meta):
        fields = BaseAttributeSerializer.Meta.fields + (
            'conditions',
            'questionsets',
            'questions',
            'tasks_as_start',
            'tasks_as_end',
            'values_count',
            'projects_count'
        )
        validators = (
            AttributeUniqueURIValidator(),
            AttributeParentValidator(),
            AttributeLockedValidator()
        )


class AttributeListSerializer(ElementExportSerializerMixin, BaseAttributeSerializer):

    xml_url = serializers.SerializerMethodField()

    class Meta(BaseAttributeSerializer.Meta):
        fields = BaseAttributeSerializer.Meta.fields + (
            'xml_url',
        )


class AttributeNestedSerializer(AttributeListSerializer):

    elements = serializers.SerializerMethodField()

    class Meta(AttributeListSerializer.Meta):
        fields = AttributeListSerializer.Meta.fields + (
            'elements',
        )

    def get_elements(self, obj):
        # get the children from the cached mptt tree
        return AttributeNestedSerializer(obj.get_children(), many=True,
                                         read_only=True, context=self.context).data


class AttributeIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'uri'
        )

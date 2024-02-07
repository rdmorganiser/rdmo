import logging

from rest_framework import serializers

from rdmo.conditions.models import Condition
from rdmo.core.serializers import ElementModelSerializerMixin, ReadOnlyObjectPermissionSerializerMixin
from rdmo.questions.models import Page, Question, QuestionSet

from ..models import Attribute
from ..validators import AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator

log = logging.getLogger(__name__)


class BaseAttributeSerializer(ElementModelSerializerMixin, ReadOnlyObjectPermissionSerializerMixin,
                              serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    read_only = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attribute
        fields = (
            'id',
            'model',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'locked',
            'read_only',
            'editors',
            'parent'
        )


class AttributeSerializer(BaseAttributeSerializer):

    key = serializers.SlugField(required=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), default=None, allow_null=True)

    conditions = serializers.PrimaryKeyRelatedField(queryset=Condition.objects.all(), required=False, many=True)
    pages = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all(), required=False, many=True)
    questionsets = serializers.PrimaryKeyRelatedField(queryset=QuestionSet.objects.all(), required=False, many=True)
    questions = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False, many=True)

    tasks = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    projects_count = serializers.IntegerField(read_only=True)
    values_count = serializers.IntegerField(read_only=True)

    class Meta(BaseAttributeSerializer.Meta):
        fields = (
            *BaseAttributeSerializer.Meta.fields,
            'conditions',
            'pages',
            'questionsets',
            'questions',
            'tasks',
            'attributes',
            'values_count',
            'projects_count'
        )
        validators = (
            AttributeUniqueURIValidator(),
            AttributeParentValidator(),
            AttributeLockedValidator()
        )

    def get_tasks(self, obj):
        return [task.id for task in obj.tasks_as_start.all()] + [task.id for task in obj.tasks_as_end.all()]

    def get_attributes(self, obj):
        return [attribute.id for attribute in obj.get_descendants()]


class AttributeListSerializer(BaseAttributeSerializer):

    class Meta(BaseAttributeSerializer.Meta):
        fields = (
            *BaseAttributeSerializer.Meta.fields,
            'is_leaf_node'
        )


class AttributeNestedSerializer(AttributeListSerializer):

    elements = serializers.SerializerMethodField()

    class Meta(AttributeListSerializer.Meta):
        fields = (
            *AttributeListSerializer.Meta.fields,
            'elements'
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

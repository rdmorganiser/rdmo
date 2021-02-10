import logging

from rest_framework import serializers
from rest_framework.reverse import reverse

from rdmo.conditions.models import Condition
from rdmo.questions.models import Question, QuestionSet
from rdmo.tasks.models import Task

from ..models import Attribute
from ..validators import (AttributeLockedValidator, AttributeParentValidator,
                          AttributeUniqueURIValidator)

log = logging.getLogger(__name__)


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'uri',
            'key',
        )


class QuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'uri',
            'path',
        )


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'uri',
            'path',
        )


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'uri',
            'key',
        )


class AttributeSerializer(serializers.ModelSerializer):

    key = serializers.SlugField(required=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), default=None, allow_null=True)
    path = serializers.CharField(required=False)
    conditions = ConditionSerializer(many=True, read_only=True)
    questionsets = QuestionSetSerializer(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    tasks_as_start = TaskSerializer(many=True, read_only=True)
    tasks_as_end = TaskSerializer(many=True, read_only=True)
    values_count = serializers.IntegerField(read_only=True)
    projects_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Attribute
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'path',
            'comment',
            'locked',
            'parent',
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


class AttributeNestedSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'path',
            'key',
            'locked',
            'children',
            'xml_url'
        )

    def get_children(self, obj):
        # get the children from the cached mptt tree
        return AttributeNestedSerializer(obj.get_children(), many=True, read_only=True).data

    def get_xml_url(self, obj):
        return reverse('v1-domain:attribute-detail-export', args=[obj.pk])


class AttributeIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'uri',
            'key',
            'path'
        )

import logging

from rest_framework import serializers
from rest_framework.reverse import reverse

from rdmo.conditions.models import Condition
from rdmo.questions.models import Question, QuestionSet
from rdmo.tasks.models import Task

from ..models import Attribute
from ..validators import AttributeUniquePathValidator

log = logging.getLogger(__name__)


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'key',
        )


class QuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'path',
        )


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'path',
        )


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'key',
        )


class AttributeSerializer(serializers.ModelSerializer):

    parent = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), default=None, allow_null=True)
    path = serializers.CharField(required=False)

    conditions = ConditionSerializer(many=True, read_only=True)
    questionsets = QuestionSetSerializer(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    tasks_as_start = TaskSerializer(many=True, read_only=True)
    tasks_as_end = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = (
            'id',
            'parent',
            'uri_prefix',
            'key',
            'path',
            'comment',
            'conditions',
            'questionsets',
            'questions',
            'tasks_as_start',
            'tasks_as_end'
        )
        validators = (AttributeUniquePathValidator(), )


class AttributeNestedSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = (
            'id',
            'uri_prefix',
            'path',
            'key',
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
            'key',
            'path'
        )

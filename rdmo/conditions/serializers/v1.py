from rest_framework import serializers
from rest_framework.reverse import reverse

from rdmo.domain.models import Attribute
from rdmo.options.models import OptionSet
from rdmo.questions.models import Question, QuestionSet
from rdmo.tasks.models import Task

from ..models import Condition
from ..validators import ConditionUniqueKeyValidator


class OptionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSet
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


class ConditionSerializer(serializers.ModelSerializer):

    source = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), required=True)

    optionsets = OptionSetSerializer(many=True, read_only=True)
    questionsets = QuestionSetSerializer(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Condition
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'source',
            'relation',
            'target_text',
            'target_option',
            'optionsets',
            'questionsets',
            'questions',
            'tasks'
        )
        validators = (ConditionUniqueKeyValidator(), )


class ConditionIndexSerializer(serializers.ModelSerializer):

    target_option_path = serializers.CharField(source='target_option.path', default=None, read_only=True)
    target_option_text = serializers.CharField(source='target_option.text', default=None, read_only=True)
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = Condition
        fields = (
            'id',
            'uri_prefix',
            'uri',
            'key',
            'comment',
            'source_path',
            'relation_label',
            'target_text',
            'target_option_path',
            'target_option_text',
            'xml_url'
        )

    def get_xml_url(self, obj):
        return reverse('v1-conditions:condition-detail-export', args=[obj.pk])

from rest_framework import serializers
from rest_framework.reverse import reverse

from rdmo.domain.models import Attribute
from rdmo.options.models import OptionSet
from rdmo.questions.models import Question, QuestionSet
from rdmo.tasks.models import Task

from ..models import Condition
from ..validators import ConditionLockedValidator, ConditionUniqueURIValidator


class OptionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri'
        )


class QuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'uri'
        )


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'uri'
        )


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'uri'
        )


class ConditionSerializer(serializers.ModelSerializer):

    key = serializers.SlugField(required=True)
    source = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), required=True)
    optionsets = OptionSetSerializer(many=True, read_only=True)
    questionsets = QuestionSetSerializer(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Condition
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'locked',
            'source',
            'relation',
            'target_text',
            'target_option',
            'optionsets',
            'questionsets',
            'questions',
            'tasks'
        )
        validators = (
            ConditionUniqueURIValidator(),
            ConditionLockedValidator()
        )


class ConditionIndexSerializer(serializers.ModelSerializer):

    target_option_uri = serializers.CharField(source='target_option.uri', default=None, read_only=True)
    target_option_text = serializers.CharField(source='target_option.text', default=None, read_only=True)
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = Condition
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'locked',
            'source_label',
            'relation_label',
            'target_text',
            'target_label',
            'target_option_uri',
            'target_option_text',
            'xml_url'
        )

    def get_xml_url(self, obj):
        return reverse('v1-conditions:condition-detail-export', args=[obj.pk])

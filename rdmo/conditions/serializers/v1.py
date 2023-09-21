from rest_framework import serializers

from rdmo.core.serializers import ElementModelSerializerMixin, ReadOnlyObjectPermissionSerializerMixin
from rdmo.domain.models import Attribute
from rdmo.options.models import OptionSet
from rdmo.questions.models import Page, Question, QuestionSet
from rdmo.tasks.models import Task

from ..models import Condition
from ..validators import ConditionLockedValidator, ConditionUniqueURIValidator


class ConditionSerializer(ElementModelSerializerMixin, ReadOnlyObjectPermissionSerializerMixin,
                          serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    uri_path = serializers.CharField(required=True)

    source = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), required=True)
    optionsets = serializers.PrimaryKeyRelatedField(queryset=OptionSet.objects.all(), required=False, many=True)
    pages = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all(), required=False, many=True)
    questionsets = serializers.PrimaryKeyRelatedField(queryset=QuestionSet.objects.all(), required=False, many=True)
    questions = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False, many=True)
    tasks = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False, many=True)

    read_only = serializers.SerializerMethodField()

    class Meta:
        model = Condition
        fields = (
            'id',
            'model',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'editors',
            'source',
            'relation',
            'target_text',
            'target_option',
            'optionsets',
            'pages',
            'questionsets',
            'questions',
            'tasks',
            'read_only'
        )
        validators = (
            ConditionUniqueURIValidator(),
            ConditionLockedValidator()
        )


class ConditionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'uri'
        )

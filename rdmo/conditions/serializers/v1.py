from rest_framework import serializers

from rdmo.core.serializers import ElementExportSerializerMixin
from rdmo.domain.models import Attribute

from ..models import Condition
from ..validators import ConditionLockedValidator, ConditionUniqueURIValidator

from rdmo.options.models import OptionSet
from rdmo.questions.models import Page, QuestionSet, Question
from rdmo.tasks.models import Task


class ConditionSerializer(serializers.ModelSerializer):

    key = serializers.SlugField(required=True)
    source = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), required=True)

    optionsets = serializers.PrimaryKeyRelatedField(queryset=OptionSet.objects.all(), required=False, many=True)
    pages = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all(), required=False, many=True)
    questionsets = serializers.PrimaryKeyRelatedField(queryset=QuestionSet.objects.all(), required=False, many=True)
    questions = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False, many=True)
    tasks = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False, many=True)

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
            'pages',
            'questionsets',
            'questions',
            'tasks'
        )
        validators = (
            ConditionUniqueURIValidator(),
            ConditionLockedValidator()
        )


class ConditionListSerializer(ElementExportSerializerMixin, ConditionSerializer):

    xml_url = serializers.SerializerMethodField()

    class Meta(ConditionSerializer.Meta):
        fields = ConditionSerializer.Meta.fields + (
            'xml_url',
        )


class ConditionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'uri'
        )

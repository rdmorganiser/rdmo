from rest_framework import serializers

from rdmo.core.serializers import ElementExportSerializerMixin
from rdmo.domain.models import Attribute

from ..models import Condition
from ..validators import ConditionLockedValidator, ConditionUniqueURIValidator


class ConditionSerializer(serializers.ModelSerializer):

    key = serializers.SlugField(required=True)
    source = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), required=True)

    optionsets = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    questionsets = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    questions = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    tasks = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

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

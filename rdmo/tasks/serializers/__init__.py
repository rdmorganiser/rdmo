from rest_framework import serializers

from rdmo.domain.models import Attribute
from rdmo.conditions.models import Condition

from rdmo.core.serializers import TranslationSerializerMixin
from rdmo.core.utils import get_language_warning

from ..models import Task
from ..validators import TaskUniqueKeyValidator


class TaskIndexSerializer(serializers.ModelSerializer):

    warning = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'key',
            'title',
            'text',
            'warning'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title') or get_language_warning(obj, 'text')


class TaskSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    key = serializers.CharField(required=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'start_attribute',
            'end_attribute',
            'days_before',
            'days_after',
            'conditions'
        )
        trans_fields = (
            'title',
            'text'
        )
        validators = (TaskUniqueKeyValidator(), )


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'path'
        )


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'key'
        )

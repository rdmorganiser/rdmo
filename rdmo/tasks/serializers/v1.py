from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin
from rdmo.core.utils import get_language_warning

from ..models import Task


class TaskSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'uri',
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


class TaskIndexSerializer(serializers.ModelSerializer):

    warning = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'uri',
            'key',
            'title',
            'text',
            'warning'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title') or get_language_warning(obj, 'text')

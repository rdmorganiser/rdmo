from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin

from ..models import Task


class TaskSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    start_attribute = serializers.CharField(source='start_attribute.uri', default=None, read_only=True)
    end_attribute = serializers.CharField(source='end_attribute.uri', default=None, read_only=True)
    conditions = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
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

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]

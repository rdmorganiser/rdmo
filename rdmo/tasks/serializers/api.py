from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin

from ..models import Task


class TaskSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    conditions = serializers.HyperlinkedRelatedField(view_name='api-v1-conditions:condition-detail', read_only=True, many=True)

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

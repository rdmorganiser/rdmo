from rest_framework import serializers

from ..models import Task


class TaskSerializer(serializers.ModelSerializer):

    conditions = serializers.HyperlinkedRelatedField(view_name='api-v1-conditions:condition-detail', read_only=True, many=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'title_en',
            'title_de',
            'text_en',
            'text_de',
            'start_attribute',
            'end_attribute',
            'days_before',
            'days_after',
            'conditions'
        )

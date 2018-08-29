from rest_framework import serializers

from ..models import Task


class TaskSerializer(serializers.ModelSerializer):

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

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]

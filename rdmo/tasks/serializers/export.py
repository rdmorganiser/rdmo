from rest_framework import serializers

from ..models import Task, TimeFrame


class ExportTimeFrameSerializer(serializers.ModelSerializer):

    start_attribute = serializers.CharField(source='start_attribute.uri')
    end_attribute = serializers.CharField(source='end_attribute.uri')

    class Meta:
        model = TimeFrame
        fields = (
            'start_attribute',
            'end_attribute',
            'days_before',
            'days_after'
        )


class TaskSerializer(serializers.ModelSerializer):

    conditions = serializers.SerializerMethodField()
    timeframe = ExportTimeFrameSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            'uri',
            'comment',
            'title_en',
            'title_de',
            'text_en',
            'text_de',
            'conditions',
            'timeframe'
        )

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]


from rest_framework import serializers

from rdmo.domain.models import Attribute
from rdmo.conditions.models import Condition

from ..models import Task, TimeFrame
from ..validators import TaskUniqueKeyValidator


class TimeFrameSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeFrame
        fields = (
            'id',
            'start_attribute',
            'end_attribute',
            'days_before',
            'days_after'
        )


class TaskSerializer(serializers.ModelSerializer):

    conditions = serializers.HyperlinkedRelatedField(view_name='api-v1-conditions:condition-detail', read_only=True, many=True)
    timeframe = TimeFrameSerializer(read_only=True)

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
            'conditions',
            'timeframe'
        )

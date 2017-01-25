from rest_framework import serializers

from .models import Task

from apps.domain.models import Attribute
from apps.conditions.models import Condition


class TaskIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'key',
            'title',
            'text'
        )


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'attribute',
            'time_period',
            'title_en',
            'title_de',
            'text_en',
            'text_de',
            'conditions'
        )


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'label',
            'value_type'
        )


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'label'
        )


class ExportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'identifier',
            'uri',
            'comment',
            'attribute',
            'time_period',
            'title_en',
            'title_de',
            'text_en',
            'text_de',
            'conditions'
        )

    def get_deadline(self, project, snapshot=None):
        values = project.values.filter(snapshot=snapshot).filter(attribute=self.attribute)

        for value in values:
            try:
                return iso8601.parse_date(value.text) + self.time_period
            except iso8601.ParseError:
                return None

from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   TranslationSerializerMixin)

from ..models import Task
from ..validators import TaskLockedValidator, TaskUniqueURIValidator


class TaskSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    key = serializers.SlugField(required=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'locked',
            'available',
            'catalogs',
            'sites',
            'groups',
            'start_attribute',
            'end_attribute',
            'days_before',
            'days_after',
            'conditions',
            'title',
            'text'
        )
        trans_fields = (
            'title',
            'text'
        )
        validators = (
            TaskUniqueURIValidator(),
            TaskLockedValidator()
        )


class TaskListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                         TaskSerializer):

    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + (
            'warning',
            'xml_url'
        )
        warning_fields = (
            'title',
        )


class TaskIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'uri'
        )

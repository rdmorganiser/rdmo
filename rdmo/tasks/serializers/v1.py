from rest_framework import serializers

from rdmo.core.serializers import (
    ElementModelSerializerMixin,
    ElementWarningSerializerMixin,
    ReadOnlyObjectPermissionSerializerMixin,
    TranslationSerializerMixin,
)

from ..models import Task
from ..validators import TaskLockedValidator, TaskUniqueURIValidator


class TaskSerializer(TranslationSerializerMixin, ElementModelSerializerMixin,
                     ElementWarningSerializerMixin, ReadOnlyObjectPermissionSerializerMixin,
                     serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    uri_path = serializers.CharField(required=True)

    warning = serializers.SerializerMethodField()
    read_only = serializers.SerializerMethodField()

    projects_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'model',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'available',
            'catalogs',
            'sites',
            'editors',
            'groups',
            'start_attribute',
            'end_attribute',
            'days_before',
            'days_after',
            'conditions',
            'title',
            'text',
            'warning',
            'read_only',
            'projects_count',
        )
        trans_fields = (
            'title',
            'text'
        )
        validators = (
            TaskUniqueURIValidator(),
            TaskLockedValidator()
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

from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementModelSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   TranslationSerializerMixin,
                                   ReadOnlyObjectPermissionsSerializerMixin)

from ..models import Task
from ..validators import TaskLockedValidator, TaskUniqueURIValidator


class BaseTaskSerializer(ReadOnlyObjectPermissionsSerializerMixin, TranslationSerializerMixin, ElementModelSerializerMixin,
                         serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    read_only = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'model',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'locked',
            'available',
            'catalogs',
            'sites',
            'editors',
            'read_only',
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


class TaskSerializer(BaseTaskSerializer):

    key = serializers.SlugField(required=True)
    projects_count = serializers.IntegerField(read_only=True)

    class Meta(BaseTaskSerializer.Meta):
        fields = BaseTaskSerializer.Meta.fields + (
            'projects_count',
        )
        validators = (
            TaskUniqueURIValidator(),
            TaskLockedValidator()
        )


class TaskListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                         BaseTaskSerializer):

    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(BaseTaskSerializer.Meta):
        fields = BaseTaskSerializer.Meta.fields + (
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

from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin, SiteSerializer
from rdmo.core.utils import get_language_warning

from ..models import Task


class TaskSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'sites',
            'groups',
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


class TaskIndexSerializer(serializers.ModelSerializer):

    sites = SiteSerializer(many=True, read_only=True)
    warning = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'uri',
            'key',
            'sites',
            'title',
            'text',
            'warning'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title') or get_language_warning(obj, 'text')

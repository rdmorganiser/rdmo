from rest_framework import serializers

from rdmo.conditions.serializers.export import ConditionExportSerializer
from rdmo.core.serializers import TranslationSerializerMixin

from ..models import Task


class TaskExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    start_attribute = serializers.CharField(source='start_attribute.uri', default=None, read_only=True)
    end_attribute = serializers.CharField(source='end_attribute.uri', default=None, read_only=True)
    conditions = ConditionExportSerializer(many=True)
    catalogs = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'start_attribute',
            'end_attribute',
            'days_before',
            'days_after',
            'conditions',
            'catalogs'
        )
        trans_fields = (
            'title',
            'text'
        )

    def get_catalogs(self, obj):
        return [catalog.uri for catalog in obj.catalogs.all()]

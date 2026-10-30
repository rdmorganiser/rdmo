from rest_framework import serializers

from rdmo.conditions.serializers.export import ConditionExportSerializer
from rdmo.core.serializers import TranslationSerializerMixin
from rdmo.domain.serializers.export import AttributeExportSerializer

from ..models import Task


class TaskExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    start_attribute = serializers.SerializerMethodField()
    end_attribute = serializers.SerializerMethodField()
    conditions = ConditionExportSerializer(many=True)
    catalogs = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'order',
            'task_type',
            'task_area',
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

    def get_start_attribute(self, obj):
        start_attribute = self.context.get('attribute_map', {}).get(obj.start_attribute_id)
        if start_attribute:
            return AttributeExportSerializer(start_attribute, context=self.context).data

    def get_end_attribute(self, obj):
        end_attribute = self.context.get('attribute_map', {}).get(obj.end_attribute_id)
        if end_attribute:
            return AttributeExportSerializer(end_attribute, context=self.context).data

    def get_catalogs(self, obj):
        return [catalog.uri for catalog in obj.catalogs.all()]

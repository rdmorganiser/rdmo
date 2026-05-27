from rest_framework import serializers

from rdmo.domain.serializers.export import AttributeExportSerializer

from ..models import Condition


class ConditionExportSerializer(serializers.ModelSerializer):

    source = serializers.SerializerMethodField()
    target_option = serializers.SerializerMethodField()

    class Meta:
        model = Condition
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'source',
            'relation',
            'target_text',
            'target_option'
        )

    def get_source(self, obj):
        source = self.context.get('attribute_map', {}).get(obj.source_id)
        if source:
            return AttributeExportSerializer(source, context=self.context).data

    def get_target_option(self, obj):
        if obj.target_option is not None:
            from rdmo.options.serializers.export import OptionExportSerializer
            return OptionExportSerializer(obj.target_option).data

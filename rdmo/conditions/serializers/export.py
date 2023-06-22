from rest_framework import serializers

from rdmo.domain.serializers.export import AttributeExportSerializer

from ..models import Condition


class ConditionExportSerializer(serializers.ModelSerializer):

    source = AttributeExportSerializer()
    target_option = serializers.SerializerMethodField()

    class Meta:
        model = Condition
        fields = (
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'source',
            'relation',
            'target_text',
            'target_option'
        )

    def get_target_option(self, obj):
        from rdmo.options.serializers.export import OptionExportSerializer
        return OptionExportSerializer(obj.target_option).data

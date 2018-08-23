from rest_framework import serializers

from ..models import Condition


class ConditionSerializer(serializers.ModelSerializer):

    source = serializers.CharField(source='source.uri', default=None, read_only=True)
    target_option = serializers.CharField(source='target_option.uri', default=None, read_only=True)

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

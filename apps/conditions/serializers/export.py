from rest_framework import serializers

from ..models import Condition


class ConditionSerializer(serializers.ModelSerializer):

    source = serializers.CharField(source='source.uri')
    target_option = serializers.CharField(source='target_option.uri')

    class Meta:
        model = Condition
        fields = (
            'uri',
            'comment',
            'source',
            'relation',
            'target_text',
            'target_option'
        )

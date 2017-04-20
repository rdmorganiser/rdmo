from rest_framework import serializers

from ..models import Condition


class ConditionSerializer(serializers.ModelSerializer):

    source = serializers.HyperlinkedRelatedField(view_name='api-v1-domain:attribute-detail', read_only=True)
    target_option = serializers.HyperlinkedRelatedField(view_name='api-v1-options:option-detail', read_only=True)

    class Meta:
        model = Condition
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'source',
            'relation',
            'target_text',
            'target_option'
        )

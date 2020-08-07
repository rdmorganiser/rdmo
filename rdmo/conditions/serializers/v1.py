from rdmo.domain.models import Attribute
from rest_framework import serializers
from rest_framework.reverse import reverse

from ..models import Condition
from ..validators import ConditionUniqueKeyValidator


class ConditionSerializer(serializers.ModelSerializer):

    key = serializers.CharField(required=True)
    source = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), required=True)

    class Meta:
        model = Condition
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'source',
            'relation',
            'target_text',
            'target_option'
        )
        validators = (ConditionUniqueKeyValidator(), )


class ConditionIndexSerializer(serializers.ModelSerializer):

    target_option_path = serializers.CharField(source='target_option.path', default=None, read_only=True)
    target_option_text = serializers.CharField(source='target_option.text', default=None, read_only=True)
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = Condition
        fields = (
            'id',
            'key',
            'comment',
            'source_path',
            'relation_label',
            'target_text',
            'target_option_path',
            'target_option_text',
            'xml_url'
        )

    def get_xml_url(self, obj):
        return reverse('v1-conditions:condition-detail-export', args=[obj.pk])

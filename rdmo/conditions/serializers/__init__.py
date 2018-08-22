from rest_framework import serializers

from rdmo.domain.models import Attribute
from rdmo.options.models import Option

from ..models import Condition
from ..validators import ConditionUniqueKeyValidator


class ConditionIndexSerializer(serializers.ModelSerializer):

    target_option_path = serializers.CharField(source='target_option.path', default=None, read_only=True)
    target_option_text = serializers.CharField(source='target_option.text', default=None, read_only=True)

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
            'target_option_text'
        )


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


class AttributeOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'order',
            'text'
        )


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'path'
        )


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'optionset',
            'order',
            'text',
            'label'
        )


class ExportSerializer(serializers.ModelSerializer):

    source = serializers.CharField(source='source.uri', default=None, read_only=True)
    target_option = serializers.CharField(source='target_option.uri', default=None, read_only=True)

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

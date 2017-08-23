from rest_framework import serializers

from rdmo.domain.models import Attribute
from rdmo.options.models import OptionSet, Option

from ..models import Condition
from ..validators import ConditionUniqueKeyValidator


class ConditionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'key',
            'comment',
            'source_path',
            'relation_label',
            'target_label'
        )


class ConditionSerializer(serializers.ModelSerializer):

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

    options = AttributeOptionSerializer(many=True)

    class Meta:
        model = Attribute
        fields = (
            'id',
            'path',
            'options'
        )


class OptionSetOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'order',
            'text'
        )


class OptionSetSerializer(serializers.ModelSerializer):

    options = OptionSetOptionSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'order',
            'options'
        )


class ExportSerializer(serializers.ModelSerializer):

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

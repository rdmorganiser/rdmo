from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   TranslationSerializerMixin)

from ...models import Option
from ...validators import OptionLockedValidator, OptionUniqueURIValidator


class BaseOptionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'text',
            'label',
            'additional_input'
        )
        trans_fields = (
            'text',
        )


class OptionSerializer(BaseOptionSerializer):

    optionsets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    values_count = serializers.IntegerField(read_only=True)
    projects_count = serializers.IntegerField(read_only=True)

    class Meta(BaseOptionSerializer.Meta):
        fields = BaseOptionSerializer.Meta.fields + (
            'optionsets',
            'conditions',
            'values_count',
            'projects_count'
        )
        validators = (
            OptionUniqueURIValidator(),
            OptionLockedValidator()
        )


class OptionListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                           BaseOptionSerializer):

    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(BaseOptionSerializer.Meta):
        fields = BaseOptionSerializer.Meta.fields + (
            'warning',
            'xml_url'
        )
        warning_fields = (
            'text',
        )


class OptionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'uri'
        )

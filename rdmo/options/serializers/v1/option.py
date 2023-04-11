from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   ThroughModelSerializerMixin,
                                   TranslationSerializerMixin)

from ...models import Option, OptionSet
from ...validators import OptionLockedValidator, OptionUniqueURIValidator


class OptionSerializer(ThroughModelSerializerMixin, TranslationSerializerMixin,
                       serializers.ModelSerializer):

    optionsets = serializers.PrimaryKeyRelatedField(queryset=OptionSet.objects.all(), required=False, many=True)
    conditions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    values_count = serializers.IntegerField(read_only=True)
    projects_count = serializers.IntegerField(read_only=True)

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
            'additional_input',
            'optionsets',
            'conditions',
            'values_count',
            'projects_count'
        )
        trans_fields = (
            'text',
        )
        parent_fields = (
            ('optionsets', 'optionset', 'option', 'optionset_options'),
        )
        validators = (
            OptionUniqueURIValidator(),
            OptionLockedValidator()
        )


class OptionListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                           OptionSerializer):

    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(OptionSerializer.Meta):
        fields = OptionSerializer.Meta.fields + (
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

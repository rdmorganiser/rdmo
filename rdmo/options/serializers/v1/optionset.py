from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ThroughModelSerializerMixin)

from ...models import OptionSet, OptionSetOption
from ...validators import OptionSetLockedValidator, OptionSetUniqueURIValidator
from .option import OptionListSerializer


class BaseOptionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'order',
            'provider_key'
        )


class OptionSetOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSetOption
        fields = (
            'option',
            'order'
        )


class OptionSetSerializer(ThroughModelSerializerMixin, BaseOptionSetSerializer):

    uri_path = serializers.CharField(required=True)
    options = OptionSetOptionSerializer(source='optionset_options', read_only=False, required=False, many=True)
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta(BaseOptionSetSerializer.Meta):
        fields = BaseOptionSetSerializer.Meta.fields + (
            'options',
            'conditions',
            'questions'
        )
        validators = (
            OptionSetUniqueURIValidator(),
            OptionSetLockedValidator()
        )
        through_fields = (
            'sections',
        )
        through_fields = (
            'options',
        )


class OptionSetListSerializer(ElementExportSerializerMixin, BaseOptionSetSerializer):

    xml_url = serializers.SerializerMethodField()

    class Meta(BaseOptionSetSerializer.Meta):
        fields = BaseOptionSetSerializer.Meta.fields + (
            'xml_url',
        )


class OptionSetNestedSerializer(OptionSetListSerializer):

    elements = serializers.SerializerMethodField()

    class Meta(OptionSetListSerializer.Meta):
        fields = OptionSetListSerializer.Meta.fields + (
            'elements',
        )

    def get_elements(self, obj):
        for element in obj.elements:
            yield OptionListSerializer(element, context=self.context).data


class OptionSetIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri'
        )

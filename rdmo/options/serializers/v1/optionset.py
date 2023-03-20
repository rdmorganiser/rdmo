from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ThroughModelListField,
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
        )


class OptionSetSerializer(ThroughModelSerializerMixin, BaseOptionSetSerializer):

    uri_path = serializers.CharField(required=True)
    options = ThroughModelListField(source='optionset_options', child=OptionSetOptionSerializer(), required=False)

    class Meta(BaseOptionSetSerializer.Meta):
        fields = BaseOptionSetSerializer.Meta.fields + (
            'options',
            'conditions'
        )
        validators = (
            OptionSetUniqueURIValidator(),
            OptionSetLockedValidator()
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

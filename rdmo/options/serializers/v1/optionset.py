from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementModelSerializerMixin,
                                   ReadOnlyObjectPermissionsSerializerMixin,
                                   ThroughModelSerializerMixin)
from rdmo.questions.models import Question

from ...models import OptionSet, OptionSetOption
from ...validators import OptionSetLockedValidator, OptionSetUniqueURIValidator
from .option import OptionListSerializer


class OptionSetOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSetOption
        fields = (
            'option',
            'order'
        )


class OptionSetSerializer(ThroughModelSerializerMixin, ElementModelSerializerMixin,
                          ReadOnlyObjectPermissionsSerializerMixin, serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    uri_path = serializers.CharField(required=True)
    options = OptionSetOptionSerializer(source='optionset_options', read_only=False, required=False, many=True)
    questions = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False, many=True)
    read_only = serializers.SerializerMethodField()

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'model',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'read_only',
            'order',
            'provider_key',
            'options',
            'conditions',
            'questions',
            'editors',
            'read_only'
        )
        through_fields = (
            ('options', 'optionset', 'option', 'optionset_options'),
        )
        validators = (
            OptionSetUniqueURIValidator(),
            OptionSetLockedValidator()
        )


class OptionSetListSerializer(ElementExportSerializerMixin, OptionSetSerializer):

    xml_url = serializers.SerializerMethodField()

    class Meta(OptionSetSerializer.Meta):
        fields = OptionSetSerializer.Meta.fields + (
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

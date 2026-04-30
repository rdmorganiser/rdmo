from rest_framework import serializers

from rdmo.config.constants import PLUGIN_TYPES
from rdmo.config.models import Plugin
from rdmo.core.serializers import (
    ElementModelSerializerMixin,
    ReadOnlyObjectPermissionSerializerMixin,
    ThroughModelSerializerMixin,
)
from rdmo.questions.models import Question

from ...models import OptionSet, OptionSetOption
from ...validators import OptionSetLockedValidator, OptionSetUniqueURIValidator
from .option import OptionSerializer


class OptionSetOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSetOption
        fields = (
            'option',
            'order'
        )


class OptionSetPluginsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plugin
        fields = (
            'uri',
            'order'
        )

class OptionSetSerializer(ThroughModelSerializerMixin, ElementModelSerializerMixin,
                          ReadOnlyObjectPermissionSerializerMixin, serializers.ModelSerializer):

    model = serializers.SerializerMethodField()

    options = OptionSetOptionSerializer(source='optionset_options', read_only=False, required=False, many=True)
    questions = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False, many=True)

    plugins = serializers.PrimaryKeyRelatedField(
        queryset=Plugin.objects.filter(plugin_type=PLUGIN_TYPES.OPTIONSET_PROVIDER), required=False, many=True
    )

    read_only = serializers.SerializerMethodField()

    condition_uris = serializers.SerializerMethodField()

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
            'options',
            'conditions',
            'questions',
            'plugins',
            'editors',
            'read_only',
            'condition_uris',
        )
        through_fields = (
            ('options', 'optionset', 'option', 'optionset_options'),
        )
        extra_kwargs = {
            'uri_path': {'required': True}
        }
        validators = (
            OptionSetUniqueURIValidator(),
            OptionSetLockedValidator()
        )

    def get_condition_uris(self, obj) -> list[str]:
        return [condition.uri for condition in obj.conditions.all()]


class OptionSetNestedSerializer(OptionSetSerializer):

    elements = serializers.SerializerMethodField()

    class Meta(OptionSetSerializer.Meta):
        fields = (
            *OptionSetSerializer.Meta.fields,
            'elements'
        )

    def get_elements(self, obj) -> list[dict]:
        for element in obj.elements:
            yield OptionSerializer(element, context=self.context).data


class OptionSetIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri'
        )

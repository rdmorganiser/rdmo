from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin
from rdmo.core.utils import get_language_warning

from ..models import OptionSet, Option
from ..validators import OptionSetUniqueKeyValidator, OptionUniquePathValidator


class OptionSetSerializer(serializers.ModelSerializer):

    key = serializers.CharField(required=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'conditions'
        )
        validators = (OptionSetUniqueKeyValidator(), )


class OptionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    key = serializers.CharField(required=True)
    optionset = serializers.PrimaryKeyRelatedField(queryset=OptionSet.objects.all(), required=True)

    class Meta:
        model = Option
        fields = (
            'id',
            'optionset',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'text',
            'additional_input'
        )
        trans_fields = (
            'text',
        )
        validators = (OptionUniquePathValidator(), )


class OptionSetIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'key',
        )
        validators = (OptionSetUniqueKeyValidator(), )


class OptionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'optionset',
            'key',
            'text',
        )


class OptionNestedSerializer(serializers.ModelSerializer):

    warning = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = (
            'id',
            'path',
            'text',
            'warning'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'text')


class OptionSetNestedSerializer(serializers.ModelSerializer):

    options = OptionNestedSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'key',
            'options'
        )

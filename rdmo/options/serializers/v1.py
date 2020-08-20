from rest_framework import serializers
from rest_framework.reverse import reverse

from rdmo.core.serializers import TranslationSerializerMixin
from rdmo.core.utils import get_language_warning

from ..models import Option, OptionSet
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
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = (
            'id',
            'uri_prefix',
            'path',
            'text',
            'warning',
            'xml_url'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'text')

    def get_xml_url(self, obj):
        return reverse('v1-options:option-detail-export', args=[obj.pk])


class OptionSetNestedSerializer(serializers.ModelSerializer):

    options = OptionNestedSerializer(many=True)
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri_prefix',
            'key',
            'options',
            'xml_url'
        )

    def get_xml_url(self, obj):
        return reverse('v1-options:optionset-detail-export', args=[obj.pk])

from rest_framework import serializers

from rdmo.core.serializers import (
    ElementModelSerializerMixin,
    ElementWarningSerializerMixin,
    MarkdownSerializerMixin,
    ReadOnlyObjectPermissionSerializerMixin,
    TranslationSerializerMixin,
)

from ..models import Plugin
from ..validators import PluginLockedValidator, PluginUniqueURIValidator


class PluginSerializer(TranslationSerializerMixin, ElementModelSerializerMixin,
                     ElementWarningSerializerMixin, ReadOnlyObjectPermissionSerializerMixin,
                     MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('title', 'text')

    model = serializers.SerializerMethodField()

    warning = serializers.SerializerMethodField()
    read_only = serializers.SerializerMethodField()

    plugin_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Plugin
        fields = (
            'id',
            'model',
            'uri',
            'uri_prefix',
            'uri_path',
            'url_name',
            'comment',
            'locked',
            'order',
            'available',
            'python_path',
            'plugin_type',
            'plugin_settings',
            'catalogs',
            'sites',
            'editors',
            'groups',
            'title',
            'warning',
            'read_only',
        )
        trans_fields = (
            'title',
        )
        extra_kwargs = {
            'uri_path': {'required': True}
        }
        validators = (
            PluginUniqueURIValidator(),
            PluginLockedValidator()
        )
        warning_fields = (
            'title',
        )

    def get_plugin_type(self, obj) -> str:
        return obj.plugin_type

class PluginIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plugin
        fields = (
            'id',
            'uri'
        )

from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers

from rdmo.core.serializers import (
    ElementModelSerializerMixin,
    ElementWarningSerializerMixin,
    MarkdownSerializerMixin,
    ReadOnlyObjectPermissionSerializerMixin,
    TranslationSerializerMixin,
)

from ..models import Plugin
from ..utils import get_plugin_python_paths
from ..validators import (
    PluginLockedValidator,
    PluginPythonPathValidator,
    PluginUniqueURIValidator,
    PluginURLNameValidator,
)


class PluginSerializer(TranslationSerializerMixin, ElementModelSerializerMixin,
                     ElementWarningSerializerMixin, ReadOnlyObjectPermissionSerializerMixin,
                     MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('title', 'text', 'help')

    model = serializers.SerializerMethodField()

    warning = serializers.SerializerMethodField()
    read_only = serializers.SerializerMethodField()

    python_path = serializers.ChoiceField(choices=get_plugin_python_paths())
    plugin_type = serializers.SerializerMethodField(read_only=True)
    plugin_meta = serializers.JSONField(read_only=True)

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
            'plugin_meta',
            'catalogs',
            'sites',
            'editors',
            'groups',
            'title',
            'help',
            'warning',
            'read_only',
        )
        trans_fields = (
            'title',
            'help',
        )
        extra_kwargs = {
            'uri_path': {'required': True}
        }
        validators = (
            PluginUniqueURIValidator(),
            PluginLockedValidator(),
            PluginPythonPathValidator(),
            PluginURLNameValidator(),
        )
        warning_fields = (
            'title',
            'help',
        )

    def get_plugin_type(self, obj) -> str:
        return obj.plugin_type

    def validate(self, attrs):
        attrs = super().validate(attrs)

        instance = self.instance or Plugin()
        for attr in ('python_path', 'plugin_settings'):
            if attr in attrs:
                setattr(instance, attr, attrs[attr])

        try:
            instance.validate_plugin_settings()
        except DjangoValidationError as e:
            if hasattr(e, 'message_dict'):
                raise serializers.ValidationError(e.message_dict) from e
            raise serializers.ValidationError(e.messages) from e

        return attrs

class PluginIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plugin
        fields = (
            'id',
            'uri'
        )

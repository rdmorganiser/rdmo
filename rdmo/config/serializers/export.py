from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin

from ..models import Plugin


class PluginExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Plugin
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'available',
            'locked',
            'order',
            'python_path',
            'plugin_settings',
            'url_name',
        )
        trans_fields = (
            'title',
            'help',
        )

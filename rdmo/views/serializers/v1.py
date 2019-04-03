from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin
from rdmo.core.utils import get_language_warning

from ..models import View


class ViewSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = View
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'template'
        )
        trans_fields = (
            'title',
            'help'
        )


class ViewIndexSerializer(serializers.ModelSerializer):

    warning = serializers.SerializerMethodField()

    class Meta:
        model = View
        fields = (
            'id',
            'uri',
            'key',
            'title',
            'help',
            'warning'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title')

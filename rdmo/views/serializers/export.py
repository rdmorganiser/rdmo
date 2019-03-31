from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin

from ..models import View


class ViewSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = View
        fields = (
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

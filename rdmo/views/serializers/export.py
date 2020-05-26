from rdmo.core.serializers import TranslationSerializerMixin
from rest_framework import serializers

from ..models import View


class ViewSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    catalogs = serializers.SerializerMethodField()

    class Meta:
        model = View
        fields = (
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'catalogs',
            'template'
        )
        trans_fields = (
            'title',
            'help'
        )

    def get_catalogs(self, obj):
        return [catalog.uri for catalog in obj.catalogs.all()]

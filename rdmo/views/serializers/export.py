from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin

from ..models import View


class ViewExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    catalogs = serializers.SerializerMethodField()

    class Meta:
        model = View
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
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

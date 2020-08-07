from rdmo.core.serializers import SiteSerializer, TranslationSerializerMixin
from rdmo.core.utils import get_language_warning
from rest_framework import serializers
from rest_framework.reverse import reverse

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
            'catalogs',
            'sites',
            'groups',
            'template'
        )
        trans_fields = (
            'title',
            'help'
        )


class ViewIndexSerializer(serializers.ModelSerializer):

    sites = SiteSerializer(many=True, read_only=True)
    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = View
        fields = (
            'id',
            'uri',
            'key',
            'sites',
            'title',
            'help',
            'warning',
            'xml_url'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title')

    def get_xml_url(self, obj):
        return reverse('v1-views:view-detail-export', args=[obj.pk])

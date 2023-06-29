from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementModelSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   ReadOnlyObjectPermissionsSerializerMixin,
                                   ThroughModelSerializerMixin,
                                   TranslationSerializerMixin)

from ...models import Catalog, CatalogSection
from ...validators import CatalogLockedValidator, CatalogUniqueURIValidator
from .section import SectionNestedSerializer


class CatalogSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatalogSection
        fields = (
            'section',
            'order'
        )


class CatalogSerializer(ThroughModelSerializerMixin, TranslationSerializerMixin,
                        ElementModelSerializerMixin, ReadOnlyObjectPermissionsSerializerMixin,
                        serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    uri_path = serializers.CharField(required=True)
    projects_count = serializers.IntegerField(read_only=True)
    sections = CatalogSectionSerializer(source='catalog_sections', read_only=False, required=False, many=True)
    read_only = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = (
            'id',
            'model',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'order',
            'available',
            'sections',
            'sites',
            'editors',
            'read_only',
            'groups',
            'title',
            'help',
            'projects_count',
        )
        trans_fields = (
            'title',
            'help'
        )
        through_fields = (
            ('sections', 'catalog', 'section', 'catalog_sections'),
        )
        validators = (
            CatalogUniqueURIValidator(),
            CatalogLockedValidator(),
        )


class CatalogListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                            CatalogSerializer):

    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(CatalogSerializer.Meta):
        fields = CatalogSerializer.Meta.fields + (
            'warning',
            'xml_url'
        )
        warning_fields = (
            'title',
        )


class CatalogNestedSerializer(CatalogListSerializer):

    elements = serializers.SerializerMethodField()

    class Meta(CatalogListSerializer.Meta):
        fields = CatalogListSerializer.Meta.fields + (
            'elements',
        )

    def get_elements(self, obj):
        for element in obj.elements:
            yield SectionNestedSerializer(element, context=self.context).data


class CatalogIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = (
            'id',
            'uri'
        )

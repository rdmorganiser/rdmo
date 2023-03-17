from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   ThroughModelListField,
                                   ThroughModelSerializerMixin,
                                   TranslationSerializerMixin)

from ...models import Catalog, CatalogSection
from ...validators import CatalogLockedValidator, CatalogUniqueURIValidator
from .section import SectionNestedSerializer


class BaseCatalogSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'order',
            'available',
            'sections',
            'sites',
            'groups',
            'title',
            'help'
        )
        trans_fields = (
            'title',
            'help'
        )


class CatalogSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatalogSection
        fields = (
            'section',
        )


class CatalogSerializer(ThroughModelSerializerMixin, BaseCatalogSerializer):

    uri_path = serializers.CharField(required=True)
    projects_count = serializers.IntegerField(read_only=True)
    sections = ThroughModelListField(source='catalog_sections', child=CatalogSectionSerializer(), required=False)

    class Meta(BaseCatalogSerializer.Meta):
        fields = BaseCatalogSerializer.Meta.fields + (
            'projects_count',
            'sections'
        )
        validators = (
            CatalogUniqueURIValidator(),
            CatalogLockedValidator(),
        )


class CatalogListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                            BaseCatalogSerializer):

    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(BaseCatalogSerializer.Meta):
        fields = BaseCatalogSerializer.Meta.fields + (
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

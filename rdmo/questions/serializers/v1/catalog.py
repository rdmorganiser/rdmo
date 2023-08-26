from rest_framework import serializers

from rdmo.core.serializers import (
    ElementModelSerializerMixin,
    ElementWarningSerializerMixin,
    ReadOnlyObjectPermissionSerializerMixin,
    ThroughModelSerializerMixin,
    TranslationSerializerMixin,
)

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
                        ElementModelSerializerMixin, ElementWarningSerializerMixin,
                        ReadOnlyObjectPermissionSerializerMixin, serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    uri_path = serializers.CharField(required=True)

    sections = CatalogSectionSerializer(source='catalog_sections', read_only=False, required=False, many=True)

    warning = serializers.SerializerMethodField()
    read_only = serializers.SerializerMethodField()

    projects_count = serializers.IntegerField(read_only=True)

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
            'groups',
            'title',
            'help',
            'warning',
            'read_only',
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
        warning_fields = (
            'title',
        )


class CatalogNestedSerializer(CatalogSerializer):

    elements = serializers.SerializerMethodField()

    class Meta(CatalogSerializer.Meta):
        fields = (
            *CatalogSerializer.Meta.fields,
            'elements'
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

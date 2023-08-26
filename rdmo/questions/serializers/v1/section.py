from rest_framework import serializers

from rdmo.core.serializers import (
    ElementModelSerializerMixin,
    ElementWarningSerializerMixin,
    ReadOnlyObjectPermissionSerializerMixin,
    ThroughModelSerializerMixin,
    TranslationSerializerMixin,
)

from ...models import Catalog, Section, SectionPage
from ...validators import SectionLockedValidator, SectionUniqueURIValidator
from .page import PageNestedSerializer


class SectionPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SectionPage
        fields = (
            'page',
            'order'
        )


class SectionSerializer(ThroughModelSerializerMixin, TranslationSerializerMixin,
                        ElementModelSerializerMixin, ElementWarningSerializerMixin,
                        ReadOnlyObjectPermissionSerializerMixin, serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    uri_path = serializers.CharField(required=True)

    catalogs = serializers.PrimaryKeyRelatedField(queryset=Catalog.objects.all(), required=False, many=True)
    pages = SectionPageSerializer(source='section_pages', read_only=False, required=False, many=True)

    warning = serializers.SerializerMethodField()
    read_only = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = (
            'id',
            'model',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'title',
            'catalogs',
            'pages',
            'editors',
            'warning',
            'read_only'
        )
        trans_fields = (
            'title',
        )
        parent_fields = (
            ('catalogs', 'catalog', 'section', 'catalog_sections'),
        )
        through_fields = (
            ('pages', 'section', 'page', 'section_pages'),
        )
        validators = (
            SectionUniqueURIValidator(),
            SectionLockedValidator()
        )
        warning_fields = (
            'title',
        )


class SectionNestedSerializer(SectionSerializer):

    elements = serializers.SerializerMethodField()

    class Meta(SectionSerializer.Meta):
        fields = (
            *SectionSerializer.Meta.fields,
            'elements'
        )

    def get_elements(self, obj):
        for element in obj.elements:
            yield PageNestedSerializer(element, context=self.context).data


class SectionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'uri'
        )

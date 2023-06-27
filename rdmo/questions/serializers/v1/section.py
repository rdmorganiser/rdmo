from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementModelSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   ReadOnlyObjectPermissionsSerializerMixin,
                                   ThroughModelSerializerMixin,
                                   TranslationSerializerMixin)

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
                        ElementModelSerializerMixin, ReadOnlyObjectPermissionsSerializerMixin,
                        serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    uri_path = serializers.CharField(required=True)
    catalogs = serializers.PrimaryKeyRelatedField(queryset=Catalog.objects.all(), required=False, many=True)
    pages = SectionPageSerializer(source='section_pages', read_only=False, required=False, many=True)
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


class SectionListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                            SectionSerializer):

    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(SectionSerializer.Meta):
        fields = SectionSerializer.Meta.fields + (
            'warning',
            'xml_url'
        )
        warning_fields = (
            'title',
        )


class SectionNestedSerializer(SectionListSerializer):

    elements = serializers.SerializerMethodField()

    class Meta(SectionListSerializer.Meta):
        fields = SectionListSerializer.Meta.fields + (
            'elements',
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

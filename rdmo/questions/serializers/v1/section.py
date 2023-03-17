from rest_framework import serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   ThroughModelListField,
                                   ThroughModelSerializerMixin,
                                   TranslationSerializerMixin)

from ...models import Section, SectionPage
from ...validators import SectionLockedValidator, SectionUniqueURIValidator
from .page import PageNestedSerializer


class BaseSectionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'locked',
            'title'
        )
        trans_fields = (
            'title',
        )


class SectionPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SectionPage
        fields = (
            'page',
        )


class SectionSerializer(ThroughModelSerializerMixin, BaseSectionSerializer):

    uri_path = serializers.CharField(required=True)
    catalogs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    pages = ThroughModelListField(source='section_pages', child=SectionPageSerializer(), required=False)

    class Meta(BaseSectionSerializer.Meta):
        fields = BaseSectionSerializer.Meta.fields + (
            'catalogs',
            'pages'
        )
        validators = (
            SectionUniqueURIValidator(),
            SectionLockedValidator()
        )


class SectionListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                            BaseSectionSerializer):

    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(BaseSectionSerializer.Meta):
        fields = BaseSectionSerializer.Meta.fields + (
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

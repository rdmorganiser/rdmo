from django.conf import settings
from rdmo.core.serializers import SiteSerializer, TranslationSerializerMixin
from rdmo.core.utils import get_language_warning
from rdmo.domain.models import Attribute
from rest_framework import serializers
from rest_framework.reverse import reverse

from ..models import Catalog, Question, QuestionSet, Section
from ..validators import (CatalogUniqueKeyValidator,
                          QuestionSetUniquePathValidator,
                          QuestionUniquePathValidator,
                          SectionUniquePathValidator)


class CatalogSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'available',
            'sites',
            'groups'
        )
        trans_fields = (
            'title',
            'help'
        )
        validators = (CatalogUniqueKeyValidator(), )


class SectionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'catalog',
            'order',
        )
        trans_fields = (
            'title',
        )
        validators = (SectionUniquePathValidator(), )


class QuestionSetSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'attribute',
            'section',
            'is_collection',
            'order',
            'conditions',
        )
        trans_fields = (
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
        )
        validators = (QuestionSetUniquePathValidator(), )


class QuestionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'attribute',
            'questionset',
            'is_collection',
            'order',
            'maximum',
            'minimum',
            'step',
            'widget_type',
            'value_type',
            'unit',
            'optionsets',
            'conditions'
        )
        trans_fields = (
            'text',
            'help',
            'verbose_name',
            'verbose_name_plural',
        )
        validators = (QuestionUniquePathValidator(), )


class CatalogIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = (
            'id',
            'title',
            'key'
        )


class SectionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'title',
            'path'
        )


class QuestionSetIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'title',
            'path',
        )


class QuestionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'text',
            'path'
        )


class AttributeNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'path'
        )


class QuestionNestedSerializer(serializers.ModelSerializer):

    warning = serializers.SerializerMethodField()
    attribute = AttributeNestedSerializer(read_only=True)
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'id',
            'uri_prefix',
            'path',
            'text',
            'attribute',
            'is_collection',
            'warning',
            'xml_url'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'text')

    def get_xml_url(self, obj):
        return reverse('v1-questions:question-detail-export', args=[obj.pk])


class QuestionSetNestedSerializer(serializers.ModelSerializer):

    questions = QuestionNestedSerializer(many=True, read_only=True)
    warning = serializers.SerializerMethodField()
    attribute = AttributeNestedSerializer(read_only=True)
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'uri_prefix',
            'path',
            'title',
            'attribute',
            'is_collection',
            'questions',
            'warning',
            'xml_url'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title')

    def get_xml_url(self, obj):
        return reverse('v1-questions:questionset-detail-export', args=[obj.pk])


class SectionNestedSerializer(serializers.ModelSerializer):

    questionsets = QuestionSetNestedSerializer(many=True, read_only=True)
    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = (
            'id',
            'uri_prefix',
            'path',
            'title',
            'questionsets',
            'warning',
            'xml_url'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title')

    def get_xml_url(self, obj):
        return reverse('v1-questions:section-detail-export', args=[obj.pk])


class CatalogNestedSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    sections = SectionNestedSerializer(many=True, read_only=True)
    sites = SiteSerializer(many=True, read_only=True)
    xml_url = serializers.SerializerMethodField()
    export_urls = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = (
            'id',
            'uri_prefix',
            'key',
            'sites',
            'title',
            'sections',
            'xml_url',
            'export_urls'
        )
        trans_fields = (
            'title',
        )

    def get_xml_url(self, obj):
        return reverse('v1-questions:catalog-detail-export', args=[obj.pk])

    def get_export_urls(self, obj):
        urls = {}
        for key, text in settings.EXPORT_FORMATS:
            urls[key] = reverse('questions_catalog_export', args=[obj.pk, key])
        return urls

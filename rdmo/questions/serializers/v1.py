from django.conf import settings
from rest_framework import serializers
from rest_framework.reverse import reverse

from rdmo.core.serializers import TranslationSerializerMixin, SiteSerializer
from rdmo.core.utils import get_language_warning
from rdmo.domain.models import Attribute

from ..models import Catalog, Question, QuestionSet, Section
from ..validators import (CatalogUniqueKeyValidator,
                          QuestionSetUniquePathValidator,
                          QuestionUniquePathValidator,
                          SectionUniquePathValidator)


class CatalogSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    key = serializers.CharField(required=True)

    class Meta:
        model = Catalog
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'sites',
            'groups'
        )
        trans_fields = (
            'title',
            'help'
        )
        validators = (CatalogUniqueKeyValidator(), )


class SectionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    key = serializers.CharField(required=True)

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

    key = serializers.CharField(required=True)

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

    key = serializers.CharField(required=True)

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
            'key',
        )


class SectionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'title',
            'path',
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
            'path',
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

    class Meta:
        model = Question
        fields = (
            'id',
            'path',
            'text',
            'attribute',
            'is_collection',
            'warning'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'text')


class QuestionSetNestedSerializer(serializers.ModelSerializer):

    questions = QuestionNestedSerializer(many=True, read_only=True)
    warning = serializers.SerializerMethodField()
    attribute = AttributeNestedSerializer(read_only=True)

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'path',
            'title',
            'attribute',
            'is_collection',
            'questions',
            'warning'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title')


class SectionNestedSerializer(serializers.ModelSerializer):

    questionsets = QuestionSetNestedSerializer(many=True, read_only=True)
    warning = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = (
            'id',
            'path',
            'title',
            'questionsets',
            'warning'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title')


class CatalogNestedSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    sections = SectionNestedSerializer(many=True, read_only=True)
    sites = SiteSerializer(many=True, read_only=True)

    urls = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = (
            'id',
            'key',
            'sites',
            'title',
            'sections',
            'urls'
        )
        trans_fields = (
            'title',
        )

    def get_urls(self, obj):
        urls = {
            'xml': reverse('questions_catalog_export', args=[obj.pk, 'xml'])
        }
        for key, text in settings.EXPORT_FORMATS:
            urls[key] = reverse('questions_catalog_export', args=[obj.pk, key])
        return urls

from django.conf import settings

from rest_framework import serializers
from rest_framework.reverse import reverse

from rdmo.core.serializers import TranslationSerializerMixin
from rdmo.core.utils import get_language_warning

from rdmo.domain.models import Attribute

from ..models import Catalog, Section, QuestionSet, Question


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'path'
        )


class QuestionSerializer(serializers.ModelSerializer):

    warning = serializers.SerializerMethodField()
    attribute = AttributeSerializer(read_only=True)

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


class QuestionSetSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True, read_only=True)
    warning = serializers.SerializerMethodField()
    attribute = AttributeSerializer(read_only=True)

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


class SectionSerializer(serializers.ModelSerializer):

    questionsets = QuestionSetSerializer(many=True, read_only=True)
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

class CatalogSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    sections = SectionSerializer(many=True, read_only=True)

    urls = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = (
            'id',
            'key',
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

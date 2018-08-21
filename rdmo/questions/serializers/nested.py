from django.conf import settings

from rest_framework import serializers
from rest_framework.reverse import reverse

from rdmo.domain.models import Attribute

from ..models import Catalog, Section, Subsection, QuestionSet, Question


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'path'
        )


class QuestionSerializer(serializers.ModelSerializer):

    attribute = AttributeSerializer(read_only=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'path',
            'text',
            'attribute',
            'is_collection',
        )


class QuestionSetSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True, read_only=True)

    attribute = AttributeSerializer(read_only=True)

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'path',
            'attribute',
            'is_collection',
            'questions'
        )


class SubsectionSerializer(serializers.ModelSerializer):

    questionsets = QuestionSetSerializer(many=True, read_only=True)

    class Meta:
        model = Subsection
        fields = (
            'id',
            'path',
            'title',
            'questionsets'
        )


class SectionSerializer(serializers.ModelSerializer):

    subsections = SubsectionSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = (
            'id',
            'path',
            'title',
            'subsections'
        )


class CatalogSerializer(serializers.ModelSerializer):

    sections = SectionSerializer(many=True, read_only=True)

    urls = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = (
            'id',
            'key',
            'title',
            'title_en',
            'title_de',
            'sections',
            'urls'
        )

    def get_urls(self, obj):
        urls = {
            'xml': reverse('questions_catalog_export', args=[obj.pk, 'xml'])
        }
        for key, text in settings.EXPORT_FORMATS:
            urls[key] = reverse('questions_catalog_export', args=[obj.pk, key])
        return urls

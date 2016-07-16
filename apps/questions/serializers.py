from django.conf import settings

from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.domain.models import AttributeEntity

from .models import *


class CatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = (
            'id',
            '__str__',
            'order',
            'title',
            'title_en',
            'title_de',
            'title'
        )


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            '__str__',
            'catalog',
            'order',
            'title',
            'title_en',
            'title_de'
        )


class SubsectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subsection
        fields = (
            'id',
            '__str__',
            'section',
            'order',
            'title',
            'title_en',
            'title_de',
        )


class QuestionEntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            '__str__',
            'attribute_entity',
            'subsection',
            'order',
            'help_en',
            'help_de',
        )


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            '__str__',
            'subsection',
            'parent_entity',
            'attribute_entity',
            'order',
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'widget_type',
        )


class NestedCatalogAttributeEntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'full_title',
        )


class NestedCatalogQuestionSerializer(serializers.ModelSerializer):

    attribute_entity = NestedCatalogAttributeEntitySerializer(read_only=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'text',
            'attribute_entity'
        )


class NestedCatalogQuestionEntitySerializer(serializers.ModelSerializer):

    questions = NestedCatalogQuestionSerializer(many=True, read_only=True)
    text = serializers.CharField(source='question.text')

    attribute_entity = NestedCatalogAttributeEntitySerializer(read_only=True)

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'subsection',
            'text',
            'is_set',
            'attribute_entity',
            'questions'
        )


class NestedCatalogSubsectionSerializer(serializers.ModelSerializer):

    entities = serializers.SerializerMethodField()

    class Meta:
        model = Subsection
        fields = (
            'id',
            'title',
            'entities'
        )

    def get_entities(self, obj):
        entities = QuestionEntity.objects.filter(subsection=obj, question__parent_entity=None).order_by('order')
        serializer = NestedCatalogQuestionEntitySerializer(instance=entities, many=True)
        return serializer.data


class NestedCatalogSectionSerializer(serializers.ModelSerializer):

    subsections = NestedCatalogSubsectionSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = (
            'id',
            'title',
            'subsections'
        )


class NestedCatalogSerializer(serializers.ModelSerializer):

    sections = NestedCatalogSectionSerializer(many=True, read_only=True)

    urls = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = (
            'id',
            'title',
            'title_en',
            'title_de',
            'sections',
            'urls'
        )

    def get_urls(self, obj):
        return {format: reverse('questions_catalog_export', args=[obj.pk, format]) for format in settings.EXPORT_FORMATS}

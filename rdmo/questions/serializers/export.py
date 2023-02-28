from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin

from ..models import (Catalog, CatalogSection, Page, PageQuestion,
                      PageQuestionSet, Question, QuestionSet,
                      QuestionSetQuestion, QuestionSetQuestionSet, Section,
                      SectionPage)


class QuestionExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    attribute = serializers.CharField(source='attribute.uri', default=None, read_only=True)
    default_option = serializers.CharField(source='default_option.uri', default=None, read_only=True)
    optionsets = serializers.SerializerMethodField()
    conditions = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'attribute',
            'is_collection',
            'is_optional',
            'default_option',
            'default_external_id',
            'widget_type',
            'value_type',
            'minimum',
            'maximum',
            'step',
            'unit',
            'width',
            'optionsets',
            'conditions'
        )
        trans_fields = (
            'help',
            'text',
            'default_text',
            'verbose_name',
            'verbose_name_plural',
        )

    def get_optionsets(self, obj):
        return [optionset.uri for optionset in obj.optionsets.all()]

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]


class QuestionSetQuestionSetExportSerializer(serializers.ModelSerializer):

    questionset = serializers.SerializerMethodField()

    class Meta:
        model = QuestionSetQuestionSet
        fields = (
            'questionset',
            'order'
        )

    def get_questionset(self, obj):
        return QuestionSetExportSerializer(obj.questionset).data


class QuestionSetQuestionExportSerializer(serializers.ModelSerializer):

    question = QuestionExportSerializer()

    class Meta:
        model = QuestionSetQuestion
        fields = (
            'question',
            'order'
        )


class QuestionSetExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    attribute = serializers.CharField(source='attribute.uri', default=None, read_only=True)
    conditions = serializers.SerializerMethodField()

    questionset_questionsets = QuestionSetQuestionSetExportSerializer(many=True, read_only=True)
    questionset_questions = QuestionSetQuestionExportSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionSet
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'attribute',
            'is_collection',
            'questionset_questionsets',
            'questionset_questions',
            'conditions'
        )
        trans_fields = (
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
        )

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]


class PageQuestionSetExportSerializer(serializers.ModelSerializer):

    questionset = QuestionSetExportSerializer()

    class Meta:
        model = PageQuestionSet
        fields = (
            'questionset',
            'order'
        )


class PageQuestionExportSerializer(serializers.ModelSerializer):

    question = QuestionExportSerializer()

    class Meta:
        model = PageQuestion
        fields = (
            'question',
            'order'
        )


class PageExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    attribute = serializers.CharField(source='attribute.uri', default=None, read_only=True)
    conditions = serializers.SerializerMethodField()

    page_questionsets = PageQuestionSetExportSerializer(many=True, read_only=True)
    page_questions = PageQuestionExportSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'attribute',
            'is_collection',
            'page_questionsets',
            'page_questions',
            'conditions'
        )
        trans_fields = (
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
        )

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]


class SectionPageExportSerializer(serializers.ModelSerializer):

    page = PageExportSerializer()

    class Meta:
        model = SectionPage
        fields = (
            'page',
            'order'
        )


class SectionExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    section_pages = SectionPageExportSerializer(many=True)

    class Meta:
        model = Section
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'section_pages'
        )
        trans_fields = (
            'title',
        )


class CatalogSectionExportSerializer(serializers.ModelSerializer):

    section = SectionExportSerializer()

    class Meta:
        model = CatalogSection
        fields = (
            'section',
            'order'
        )


class CatalogExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    catalog_sections = CatalogSectionExportSerializer(many=True)

    class Meta:
        model = Catalog
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'order',
            'catalog_sections'
        )
        trans_fields = (
            'title',
            'help'
        )

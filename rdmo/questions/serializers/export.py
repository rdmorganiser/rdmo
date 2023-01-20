from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin

from ..models import Catalog, Question, Page, QuestionSet, Section


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
            'order',
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


class QuestionSetExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    attribute = serializers.CharField(source='attribute.uri', default=None, read_only=True)
    questionsets = serializers.SerializerMethodField()
    questions = QuestionExportSerializer(many=True, read_only=True)
    conditions = serializers.SerializerMethodField()

    class Meta:
        model = QuestionSet
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'attribute',
            'is_collection',
            'order',
            'questionsets',
            'questions',
            'conditions'
        )
        trans_fields = (
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
        )

    def get_questionsets(self, obj):
        return QuestionSetExportSerializer(obj.questionsets, many=True).data

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]


class PageExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    attribute = serializers.CharField(source='attribute.uri', default=None, read_only=True)
    questionsets = QuestionSetExportSerializer(many=True, read_only=True)
    questions = QuestionExportSerializer(many=True, read_only=True)
    conditions = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'attribute',
            'is_collection',
            'order',
            'questionsets',
            'questions',
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


class SectionExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    pages = PageExportSerializer(many=True)

    class Meta:
        model = Section
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'order',
            'pages'
        )
        trans_fields = (
            'title',
        )


class CatalogExportSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    sections = SectionExportSerializer(many=True)

    class Meta:
        model = Catalog
        fields = (
            'uri',
            'uri_prefix',
            'uri_path',
            'comment',
            'order',
            'sections'
        )
        trans_fields = (
            'title',
            'help'
        )

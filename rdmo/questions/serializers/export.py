from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin

from ..models import Catalog, Section, QuestionSet, Question


class QuestionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    attribute = serializers.CharField(source='attribute.uri', default=None, read_only=True)
    questionset = serializers.CharField(source='questionset.uri', default=None, read_only=True)
    optionsets = serializers.SerializerMethodField()
    conditions = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'uri',
            'uri_prefix',
            'key',
            'path',
            'comment',
            'attribute',
            'questionset',
            'is_collection',
            'order',
            'widget_type',
            'value_type',
            'minimum',
            'maximum',
            'step',
            'unit',
            'optionsets',
            'conditions'
        )
        trans_fields = (
            'help',
            'text',
            'verbose_name',
            'verbose_name_plural',
        )

    def get_optionsets(self, obj):
        return [optionset.uri for optionset in obj.optionsets.all()]

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]


class QuestionSetSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    attribute = serializers.CharField(source='attribute.uri', default=None, read_only=True)
    section = serializers.CharField(source='section.uri', default=None, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    conditions = serializers.SerializerMethodField()

    class Meta:
        model = QuestionSet
        fields = (
            'uri',
            'uri_prefix',
            'key',
            'path',
            'comment',
            'attribute',
            'section',
            'is_collection',
            'order',
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


class SectionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    catalog = serializers.CharField(source='catalog.uri', default=None, read_only=True)
    questionsets = QuestionSetSerializer(many=True)

    class Meta:
        model = Section
        fields = (
            'uri',
            'uri_prefix',
            'key',
            'path',
            'comment',
            'catalog',
            'order',
            'questionsets'
        )
        trans_fields = (
            'title',
        )


class CatalogSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    sections = SectionSerializer(many=True)

    class Meta:
        model = Catalog
        fields = (
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'sections'
        )
        trans_fields = (
            'title',
        )

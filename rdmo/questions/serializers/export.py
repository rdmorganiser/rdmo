from rest_framework import serializers

from ..models import Catalog, Section, QuestionSet, Question


class QuestionSerializer(serializers.ModelSerializer):

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
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'verbose_name_en',
            'verbose_name_de',
            'verbose_name_plural_en',
            'verbose_name_plural_de',
            'widget_type',
            'value_type',
            'minimum',
            'maximum',
            'step',
            'unit',
            'optionsets',
            'conditions'
        )

    def get_optionsets(self, obj):
        return [optionset.uri for optionset in obj.optionsets.all()]

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]


class QuestionSetSerializer(serializers.ModelSerializer):

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
            'title_en',
            'title_de',
            'help_en',
            'help_de',
            'verbose_name_en',
            'verbose_name_de',
            'verbose_name_plural_en',
            'verbose_name_plural_de',
            'questions',
            'conditions'
        )

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]


class SectionSerializer(serializers.ModelSerializer):

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
            'title',
            'title_en',
            'title_de',
            'questionsets'
        )


class CatalogSerializer(serializers.ModelSerializer):

    sections = SectionSerializer(many=True)

    class Meta:
        model = Catalog
        fields = (
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'title',
            'title_en',
            'title_de',
            'sections'
        )

from rest_framework import serializers

from ..models import Catalog, Section, Subsection, QuestionSet, Question


class CatalogSerializer(serializers.ModelSerializer):

    sections = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:section-detail', read_only=True, many=True)

    class Meta:
        model = Catalog
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'title_en',
            'title_de',
            'sections'
        )


class SectionSerializer(serializers.ModelSerializer):

    catalog = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:catalog-detail', read_only=True)
    subsections = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:subsection-detail', read_only=True, many=True)

    class Meta:
        model = Section
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'path',
            'key',
            'comment',
            'catalog',
            'order',
            'title_en',
            'title_de',
            'subsections'
        )


class SubsectionSerializer(serializers.ModelSerializer):

    section = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:section-detail', read_only=True)
    questionsets = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:questionset-detail', read_only=True, many=True)

    class Meta:
        model = Subsection
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'section',
            'order',
            'title_en',
            'title_de',
            'questionsets'
        )


class QuestionSetSerializer(serializers.ModelSerializer):

    subsection = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:subsection-detail', read_only=True)
    questions = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:question-detail', read_only=True, many=True)

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'attribute',
            'subsection',
            'is_collection',
            'order',
            'help_en',
            'help_de',
            'questions'
        )


class QuestionSerializer(serializers.ModelSerializer):

    questionset = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:questionset-detail', read_only=True)
    optionsets = serializers.HyperlinkedRelatedField(view_name='api-v1-options:optionset-detail', read_only=True, many=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'uri',
            'key',
            'comment',
            'attribute',
            'questionset',
            'is_collection',
            'order',
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'widget_type',
            'value_type',
            'unit',
            'optionsets'
        )

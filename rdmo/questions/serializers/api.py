from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin

from ..models import Catalog, Section, QuestionSet, Question


class CatalogSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

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
            'sections'
        )
        trans_fields = (
            'title',
        )


class SectionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    catalog = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:catalog-detail', read_only=True)
    questionsets = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:questionset-detail', read_only=True, many=True)

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
            'questionsets'
        )
        trans_fields = (
            'title',
        )


class QuestionSetSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    section = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:section-detail', read_only=True)
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
            'section',
            'is_collection',
            'order',
            'questions'
        )
        trans_fields = (
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
        )


class QuestionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

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
            'widget_type',
            'value_type',
            'unit',
            'optionsets'
        )
        trans_fields = (
            'help',
            'text',
            'verbose_name',
            'verbose_name_plural',
        )

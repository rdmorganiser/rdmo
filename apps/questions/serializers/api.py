from rest_framework import serializers

from ..models import Catalog, Section, Subsection, QuestionEntity, Question


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
    question_entities = serializers.SerializerMethodField()

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
            'question_entities'
        )

    def get_question_entities(self, obj):

        question_entities = []
        for entity in obj.entities.all():
            if hasattr(entity, 'question'):
                field = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:question-detail', read_only=True)
            else:
                field = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:questionset-detail', read_only=True)

            field.context = self.context
            question_entities.append(field.to_representation(entity))

        return question_entities


class QuestionSetSerializer(serializers.ModelSerializer):

    subsection = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:subsection-detail', read_only=True)
    questions = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:question-detail', read_only=True, many=True)

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'subsection',
            'attribute_entity',
            'order',
            'help_en',
            'help_de',
            'questions'
        )


class QuestionSerializer(serializers.ModelSerializer):

    subsection = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:subsection-detail', read_only=True)
    questionset = serializers.HyperlinkedRelatedField(source='parent', view_name='api-v1-questions:questionset-detail', read_only=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'uri',
            'key',
            'comment',
            'subsection',
            'questionset',
            'attribute_entity',
            'order',
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'widget_type',
        )

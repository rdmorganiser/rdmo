from rest_framework import serializers

from ..models import Catalog, Section, Subsection, QuestionEntity, Question


class QuestionSerializer(serializers.ModelSerializer):

    attribute_entity = serializers.CharField(source='attribute_entity.uri')

    class Meta:
        model = Question
        fields = (
            'parent',
            'attribute_entity',
            'uri',
            'comment',
            'order',
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'widget_type'
        )


class QuestionEntitySerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True, read_only=True)
    text_en = serializers.CharField(source='question.text_en')
    text_de = serializers.CharField(source='question.text_de')
    widget_type = serializers.CharField(source='question.widget_type')

    attribute_entity = serializers.CharField(source='attribute_entity.uri')

    class Meta:
        model = QuestionEntity
        fields = (
            'uri',
            'comment',
            'text_en',
            'text_de',
            'is_set',
            'attribute_entity',
            'order',
            'help_en',
            'help_de',
            'widget_type',
            'questions'
        )


class SubsectionSerializer(serializers.ModelSerializer):

    entities = serializers.SerializerMethodField()

    class Meta:
        model = Subsection
        fields = (
            'uri',
            'comment',
            'order',
            'title_en',
            'title_de',
            'entities'
        )

    def get_entities(self, obj):
        entities = QuestionEntity.objects.filter(subsection=obj, question__parent=None)
        serializer = QuestionEntitySerializer(instance=entities, many=True)
        return serializer.data


class SectionSerializer(serializers.ModelSerializer):

    subsections = SubsectionSerializer(many=True)

    class Meta:
        model = Section
        fields = (
            'uri',
            'comment',
            'order',
            'title',
            'title_en',
            'title_de',
            'subsections'
        )


class CatalogSerializer(serializers.ModelSerializer):

    sections = SectionSerializer(many=True)

    class Meta:
        model = Catalog
        fields = (
            'uri',
            'comment',
            'order',
            'title',
            'title_en',
            'title_de',
            'sections'
        )

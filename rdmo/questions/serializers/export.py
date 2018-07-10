from rest_framework import serializers

from ..models import Catalog, Section, Subsection, QuestionEntity, Question


class QuestionSerializer(serializers.ModelSerializer):

    attribute_entity = serializers.CharField(source='attribute_entity.uri', default=None)

    class Meta:
        model = Question
        fields = (
            'parent',
            'attribute_entity',
            'is_collection',
            'uri',
            'comment',
            'order',
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'widget_type',
            'value_type',
            'unit'
        )


class QuestionEntitySerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True, read_only=True)
    text_en = serializers.CharField(source='question.text_en', default=None)
    text_de = serializers.CharField(source='question.text_de', default=None)
    widget_type = serializers.CharField(source='question.widget_type', default=None)
    value_type = serializers.CharField(source='question.value_type', default=None)
    unit = serializers.CharField(source='question.unit', default=None)

    attribute_entity = serializers.CharField(source='attribute_entity.uri', default=None)
    optionsets = serializers.SerializerMethodField()
    conditions = serializers.SerializerMethodField()

    class Meta:
        model = QuestionEntity
        fields = (
            'uri',
            'comment',
            'text_en',
            'text_de',
            'is_set',
            'attribute_entity',
            'is_collection',
            'order',
            'help_en',
            'help_de',
            'widget_type',
            'value_type',
            'unit',
            'questions',
            'optionsets',
            'conditions'
        )

    def get_optionsets(self, obj):
        try:
            return [option.uri for option in obj.question.optionsets.all()]
        except Question.DoesNotExist:
            return None

    def get_conditions(self, obj):
        return [condition.uri for condition in obj.conditions.all()]


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

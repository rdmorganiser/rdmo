from rest_framework import serializers

from apps.domain.models import Attribute, Option, Condition

from .models import *


class NestedQuestionSerializer(serializers.ModelSerializer):

    # attribute = NestedAttributeSerializer(read_only=True)
    # options = NestedOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'text',
            'help',
            # 'attribute',
            'widget_type',
            'is_collection',
            # 'options'
        )


class NestedQuestionEntitySerializer(serializers.ModelSerializer):

    questions = NestedQuestionSerializer(source='questionset.questions', many=True, read_only=True)
    text = serializers.CharField(source='question.text')

    # attribute = NestedAttributeSerializer(source='question.attribute', read_only=True)
    # attributeset = NestedAttributeSetSerializer(source='questionset.attributeset', read_only=True)

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'subsection',
            'title',
            'text',
            'is_set',
            'is_collection',
            # 'attribute',
            # 'attributeset',
            'questions'
        )


class NestedSubsectionSerializer(serializers.ModelSerializer):

    entities = serializers.SerializerMethodField()

    class Meta:
        model = Subsection
        fields = ('id', 'title', 'entities')

    def get_entities(self, obj):
        entities = QuestionEntity.objects.filter(subsection=obj, question__questionset=None)
        serializer = NestedQuestionEntitySerializer(instance=entities, many=True)
        return serializer.data


class NestedSectionSerializer(serializers.ModelSerializer):

    subsections = NestedSubsectionSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ('id', 'title', 'subsections')


class NestedCatalogSerializer(serializers.ModelSerializer):

    sections = NestedSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = ('id', 'title', 'title_en', 'title_de', 'sections')


class CatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = ('id', 'title', 'title_en', 'title_de')


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'catalog',
            'order',
            'title_en',
            'title_de'
        )


class SubsectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subsection
        fields = (
            'id',
            'section',
            'order',
            'title_en',
            'title_de'
        )


class QuestionEntitySerializer(serializers.ModelSerializer):

    questions = NestedQuestionSerializer(many=True, read_only=True)
    text = serializers.CharField(source='question.text')
    widget_type = serializers.CharField(source='question.widget_type')

    next = serializers.SerializerMethodField()
    prev = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    section = serializers.CharField(source='subsection.section.title')
    subsection = serializers.CharField(source='subsection.title')

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'order',
            'text',
            'help',
            'questions',
            'widget_type',
            'next',
            'prev',
            'progress',
            'section',
            'subsection',
        )

    def get_prev(self, obj):
        try:
            return QuestionEntity.objects.get_prev(obj.pk).pk
        except QuestionEntity.DoesNotExist:
            return None

    def get_next(self, obj):
        try:
            return QuestionEntity.objects.get_next(obj.pk).pk
        except QuestionEntity.DoesNotExist:
            return None

    def get_progress(self, obj):
        try:
            return QuestionEntity.objects.get_progress(obj.pk)
        except QuestionEntity.DoesNotExist:
            return None


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'parent_entity',
            'subsection',
            'order',
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'widget_type',
        )

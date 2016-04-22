from rest_framework import serializers

from .models import *


class NestedQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'text', 'tag')


class NestedQuestionEntitySerializer(serializers.ModelSerializer):

    text = serializers.SerializerMethodField()
    questions = NestedQuestionSerializer(source='questionset.questions', many=True, read_only=True)

    class Meta:
        model = QuestionEntity
        fields = ('id', 'title', 'text', 'is_set', 'is_collection', 'tag', 'questions')

    def get_text(self, obj):
        if obj.is_set:
            return None
        else:
            return obj.question.text


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

    text = serializers.SerializerMethodField()
    questions = NestedQuestionSerializer(source='questionset.questions', many=True, read_only=True)

    class Meta:
        model = QuestionEntity
        fields = ('id', 'title', 'text', 'is_set', 'is_collection', 'tag', 'questions')

    def get_text(self, obj):
        if obj.is_set:
            return None
        else:
            return obj.question.text


class QuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'subsection',
            'order',
            'title_en',
            'title_de',
            'help_en',
            'help_de',
            'attributeset'
        )


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'subsection',
            'order',
            'title_en',
            'title_de',
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'attribute',
            'questionset',
            'widget_type'
        )


class WidgetTypeSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj[0]

    def get_text(self, obj):
        return obj[1]

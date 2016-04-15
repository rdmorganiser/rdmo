from rest_framework import serializers

from .models import *


class CatalogQuestionSerializer(serializers.ModelSerializer):

    tag = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('id', 'text', 'tag')

    def get_tag(self, obj):
        return obj.attribute.tag


class CatalogQuestionEntitiesSerializer(serializers.ModelSerializer):

    text = serializers.CharField(source='question.text', read_only=True)
    questions = CatalogQuestionSerializer(source='questionset.questions', many=True, read_only=True)
    tag = serializers.SerializerMethodField()

    class Meta:
        model = QuestionEntity
        fields = ('id', 'title', 'text', 'is_set', 'questions', 'tag')

    def get_tag(self, obj):
        if obj.is_set:
            return obj.questionset.attributeset.tag
        else:
            return obj.question.attribute.tag


class CatalogSubsectionSerializer(serializers.ModelSerializer):

    entities = CatalogQuestionEntitiesSerializer(many=True, read_only=True)

    class Meta:
        model = Subsection
        fields = ('id', 'title', 'entities')


class CatalogSectionSerializer(serializers.ModelSerializer):

    subsections = CatalogSubsectionSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ('id', 'title', 'subsections')


class CatalogSerializer(serializers.ModelSerializer):

    sections = CatalogSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = ('id', 'title', 'sections')


class CatalogListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = ('id', 'title')

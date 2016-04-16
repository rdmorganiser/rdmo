from rest_framework import serializers

from .models import *

class QuestionSerializer(serializers.ModelSerializer):

    tag = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('id', 'text', 'tag')

    def get_tag(self, obj):
        if obj.question.attribute:
            return obj.question.attribute.tag
        else:
            return None


class QuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = ('id', 'title')


class QuestionEntitySerializer(serializers.ModelSerializer):

    text = serializers.CharField(source='question.text', read_only=True)
    questions = QuestionSerializer(source='questionset.questions', many=True, read_only=True)
    tag = serializers.SerializerMethodField()
    is_collection = serializers.SerializerMethodField()

    class Meta:
        model = QuestionEntity
        fields = ('id', 'title', 'text', 'is_set', 'is_collection', 'questions', 'tag')

    def get_tag(self, obj):
        if obj.is_set:
            if obj.questionset.attributeset:
                return obj.questionset.attributeset.tag
            else:
                return None
        else:
            if obj.question.attribute:
                return obj.question.attribute.tag
            else:
                return None

    def get_is_collection(self, obj):
        if obj.is_set:
            if obj.questionset.attributeset:
                return obj.questionset.attributeset.is_collection
            else:
                return None
        else:
            if obj.question.attribute:
                return obj.question.attribute.is_collection
            else:
                return None

class SubsectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subsection
        fields = ('id', 'title')


class SectionSerializer(serializers.ModelSerializer):

    subsections = SubsectionSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ('id', 'title', 'subsections')


class CatalogSerializer(serializers.ModelSerializer):

    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = ('id', 'title', 'title_en', 'title_de', 'sections')

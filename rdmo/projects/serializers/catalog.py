from rest_framework import serializers

from rdmo.questions.models import Catalog, Section, QuestionSet, Question


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'text'
        )


class QuestionSetSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'title',
            'questions'
        )


class SectionSerializer(serializers.ModelSerializer):

    questionsets = QuestionSetSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = (
            'id',
            'title',
            'questionsets'
        )


class CatalogSerializer(serializers.ModelSerializer):

    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = (
            'id',
            'title',
            'sections'
        )

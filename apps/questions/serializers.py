from markdown import markdown as markdown_function

from django.utils.encoding import force_text

from rest_framework import serializers

from apps.domain.models import AttributeEntity
from apps.domain.serializers import AttributeSerializer, AttributeEntitySerializer, ConditionSerializer


from .models import *


class NestedAttributeEntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'full_title',
        )


class NestedQuestionSerializer(serializers.ModelSerializer):

    attribute_entity = NestedAttributeEntitySerializer(read_only=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'text',
            'attribute_entity'
        )


class NestedQuestionEntitySerializer(serializers.ModelSerializer):

    questions = NestedQuestionSerializer(many=True, read_only=True)
    text = serializers.CharField(source='question.text')

    attribute_entity = NestedAttributeEntitySerializer(read_only=True)

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'subsection',
            'text',
            'is_set',
            'attribute_entity',
            'questions'
        )


class NestedSubsectionSerializer(serializers.ModelSerializer):

    entities = serializers.SerializerMethodField()

    class Meta:
        model = Subsection
        fields = ('id', 'title', 'entities')

    def get_entities(self, obj):
        entities = QuestionEntity.objects.filter(subsection=obj, question__parent_entity=None).order_by('order')
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
        fields = (
            'id',
            '__str__',
            'order',
            'title_en',
            'title_de',
            'title'
        )


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            '__str__',
            'catalog',
            'order',
            'title',
            'title_en',
            'title_de'
        )


class SubsectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subsection
        fields = (
            'id',
            '__str__',
            'section',
            'order',
            'title',
            'title_en',
            'title_de',
        )


class QuestionEntityQuestionSerializer(serializers.ModelSerializer):

    attribute = AttributeSerializer(source='attribute_entity.attribute')

    class Meta:
        model = Question
        fields = (
            'id',
            '__str__',
            'order',
            'text',
            'help',
            'widget_type',
            'attribute',
        )


class QuestionEntitySerializer(serializers.ModelSerializer):

    questions = QuestionEntityQuestionSerializer(many=True, read_only=True)
    text = serializers.CharField(source='question.text')
    widget_type = serializers.CharField(source='question.widget_type')

    next = serializers.SerializerMethodField()
    prev = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    title_attribute = serializers.SerializerMethodField()

    section = serializers.CharField(source='subsection.section.title')
    subsection = serializers.CharField(source='subsection.title')

    attribute_entity = serializers.SerializerMethodField()
    attribute = serializers.SerializerMethodField()

    conditions = ConditionSerializer(source='attribute_entity.conditions', many=True, read_only=True)

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            '__str__',
            'order',
            'text',
            'help',
            'questions',
            'widget_type',
            'is_set',
            'title_attribute',
            'next',
            'prev',
            'progress',
            'section',
            'subsection',
            'attribute_entity',
            'attribute',
            'conditions'
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

    def get_title_attribute(self, obj):
        try:
            attribute = obj.attribute_entity.children.get(title='id')
            return {'id': attribute.pk}
        except AttributeEntity.DoesNotExist:
            return None

    def get_attribute_entity(self, obj):
        if obj.attribute_entity.is_attribute:
            return None
        else:
            return AttributeEntitySerializer(instance=obj.attribute_entity).data

    def get_attribute(self, obj):
        if obj.attribute_entity.is_attribute:
            return AttributeSerializer(instance=obj.attribute_entity.attribute).data
        else:
            return None

    def to_representation(self, instance):
        response = super(QuestionEntitySerializer, self).to_representation(instance)

        if 'help' in response and response['help']:
            response['help'] = markdown_function(force_text(response['help']))

        return response


class QuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            '__str__',
            'attribute_entity',
            'subsection',
            'order',
            'help_en',
            'help_de',
        )


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            '__str__',
            'subsection',
            'parent_entity',
            'attribute_entity',
            'order',
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'widget_type',
        )

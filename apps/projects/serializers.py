from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from apps.core.serializers import MarkdownSerializerMixin
from apps.conditions.models import Condition
from apps.domain.models import AttributeEntity, Attribute, Option, Range, VerboseName
from apps.questions.models import Catalog, Section, Subsection, QuestionEntity, Question

from .models import *


class ProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'current_snapshot', 'catalog')


class ValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Value
        fields = (
            'id',
            'snapshot',
            'attribute',
            'set_index',
            'collection_index',
            'text',
            'option'
        )


class QuestionEntityOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'text',
            'additional_input'
        )


class QuestionEntityRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Range
        fields = (
            'id',
            'minimum',
            'maximum',
            'step'
        )


class QuestionEntityQuestionVerboseNameSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    name_plural = serializers.SerializerMethodField()

    class Meta:
        model = VerboseName
        fields = (
            'name',
            'name_plural'
        )

    def get_name(self, obj):
        return obj.name or _('set')

    def get_name_plural(self, obj):
        return obj.name_plural or _('sets')


class QuestionEntityVerboseNameSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    name_plural = serializers.SerializerMethodField()

    class Meta:
        model = VerboseName
        fields = (
            'name',
            'name_plural'
        )

    def get_name(self, obj):
        return obj.name or _('item')

    def get_name_plural(self, obj):
        return obj.name_plural or _('items')


class QuestionEntityAttributeSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    options = QuestionEntityOptionSerializer(many=True, read_only=True)
    range = QuestionEntityRangeSerializer(read_only=True)
    verbosename = QuestionEntityQuestionVerboseNameSerializer()

    class Meta:
        model = Attribute
        fields = (
            'id',
            'options',
            'range',
            'verbosename',
            'is_collection'
        )


class QuestionEntityAttributeEntitySerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    verbosename = QuestionEntityVerboseNameSerializer()

    id_attribute = serializers.SerializerMethodField()

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'id_attribute',
            'verbosename',
        )

    def get_id_attribute(self, obj):
        try:
            return {'id': obj.children.get(title='id').pk}
        except AttributeEntity.DoesNotExist:
            return None


class QuestionEntityConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'source',
            'relation',
            'target_text',
            'target_option'
        )


class QuestionEntityQuestionSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('help', )

    attribute = QuestionEntityAttributeSerializer(source='attribute_entity.attribute')

    class Meta:
        model = Question
        fields = (
            'id',
            'order',
            'text',
            'help',
            'widget_type',
            'attribute'
        )


class QuestionEntitySerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('help', )

    attribute_entity = QuestionEntityAttributeEntitySerializer()

    collection = QuestionEntityAttributeEntitySerializer(source='attribute_entity.parent_collection')

    questions = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    next = serializers.SerializerMethodField()
    prev = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    section = serializers.SerializerMethodField()
    subsection = serializers.SerializerMethodField()

    conditions = QuestionEntityConditionSerializer(source='attribute_entity.conditions', many=True)

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'help',
            'attribute_entity',
            'collection',
            'is_set',
            'next',
            'prev',
            'progress',
            'section',
            'subsection',
            'collection',
            'questions',
            'attributes',
            'conditions'
        )

    def get_questions(self, obj):
        if obj.is_set:
            return QuestionEntityQuestionSerializer(instance=obj.questions, many=True, read_only=True).data
        else:
            return [QuestionEntityQuestionSerializer(instance=obj.question, read_only=True).data]

    def get_attributes(self, obj):
        if obj.is_set:
            if obj.attribute_entity.parent_collection_id:
                attributes = Attribute.objects.filter(parent_collection_id=obj.attribute_entity.parent_collection_id)
                return [attribute.id for attribute in attributes]
            else:
                return [question.attribute_entity_id for question in obj.questions.all()]
        else:
            return [obj.attribute_entity_id]

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

    def get_section(self, obj):
        return {
            'id': obj.subsection.section.id,
            'title': obj.subsection.section.title
        }

    def get_subsection(self, obj):
        return {
            'id': obj.subsection.id,
            'title': obj.subsection.title
        }


class CatalogQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'text'
        )


class CatalogQuestionEntitySerializer(serializers.ModelSerializer):

    questions = CatalogQuestionSerializer(many=True, read_only=True)
    text = serializers.CharField(source='question.text')

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'text',
            'questions'
        )


class CatalogSubsectionSerializer(serializers.ModelSerializer):

    entities = serializers.SerializerMethodField()

    class Meta:
        model = Subsection
        fields = (
            'id',
            'title',
            'entities'
        )

    def get_entities(self, obj):
        entities = QuestionEntity.objects.filter(subsection=obj, question__parent_entity=None).order_by('order')
        return CatalogQuestionEntitySerializer(instance=entities, many=True).data


class CatalogSectionSerializer(serializers.ModelSerializer):

    subsections = CatalogSubsectionSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = (
            'id',
            'title',
            'subsections'
        )


class CatalogSerializer(serializers.ModelSerializer):

    sections = CatalogSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = (
            'id',
            'title',
            'sections'
        )

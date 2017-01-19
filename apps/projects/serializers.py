from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from apps.core.serializers import MarkdownSerializerMixin
from apps.conditions.models import Condition
from apps.domain.models import AttributeEntity, Attribute, Range
from apps.options.models import OptionSet, Option
from apps.questions.models import Catalog, Section, Subsection, QuestionEntity, Question

from .models import *


class ProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'catalog'
        )


class ValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Value
        fields = (
            'id',
            'created',
            'updated',
            'project',
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


class QuestionEntityOptionSetSerializer(serializers.ModelSerializer):

    options = QuestionEntityOptionSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'options',
            'conditions'
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


class QuestionEntityAttributeSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    range = QuestionEntityRangeSerializer(read_only=True)
    verbosename = serializers.SerializerMethodField()
    optionsets = QuestionEntityOptionSetSerializer(many=True)

    class Meta:
        model = Attribute
        fields = (
            'id',
            'optionsets',
            'range',
            'verbosename',
            'optionsets',
            'is_collection'
        )

    def get_verbosename(self, obj):
        if hasattr(obj, 'verbosename'):
            return {
                'name': obj.verbosename.name,
                'name_plural': obj.verbosename.name_plural
            }
        else:
            return {
                'name': _('item'),
                'name_plural': _('items')
            }


class QuestionEntityAttributeEntitySerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    verbosename = serializers.SerializerMethodField()

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
            return {'id': obj.children.get(key='id').pk}
        except AttributeEntity.DoesNotExist:
            return None

    def get_verbosename(self, obj):
        if hasattr(obj, 'verbosename'):
            return {
                'name': obj.verbosename.name,
                'name_plural': obj.verbosename.name_plural
            }
        else:
            return {
                'name': _('set'),
                'name_plural': _('sets')
            }


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

    collection = serializers.SerializerMethodField()

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
            if obj.attribute_entity:
                if obj.attribute_entity.parent_collection_id:
                    attributes = Attribute.objects.filter(parent_collection_id=obj.attribute_entity.parent_collection_id)
                    return [attribute.id for attribute in attributes]
                else:
                    return [question.attribute_entity_id for question in obj.questions.all()]
            else:
                return []
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

    def get_collection(self, obj):
        if obj.attribute_entity.parent_collection:
            QuestionEntityAttributeEntitySerializer(instance=obj.attribute_entity.parent_collection).data
        elif obj.attribute_entity.is_collection and not obj.attribute_entity.is_attribute:
            return QuestionEntityAttributeEntitySerializer(instance=obj.attribute_entity).data
        else:
            return None


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
        entities = QuestionEntity.objects.filter(subsection=obj, question__parent=None).order_by('order')
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


class ExportAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'identifier',
        )


class ExportOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'identifier',
        )


class ExportValueSerializer(serializers.ModelSerializer):

    attribute = ExportAttributeSerializer()
    option = ExportOptionSerializer()

    class Meta:
        model = Value
        fields = (
            'id',
            'created',
            'updated',
            'project',
            'snapshot',
            'attribute',
            'set_index',
            'collection_index',
            'text',
            'option'
        )


class ExportProjectsSerializer(serializers.ModelSerializer):

    values = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'catalog',
            'values'
        )

    def get_values(self, obj):
        values = Value.objects.filter(Snapshot=none)
        serializer = ExportValueSerializer(instance=values, many=True)
        return serializer.data


class ExportSnapshotSerializer(serializers.ModelSerializer):

    values = serializers.SerializerMethodField()

    class Meta:
        model = Snapshot
        fields = (
            'title',
            'description',
            'project',
            'values'
        )

    def get_values(self, obj):
        values = Value.objects.filter(snapshot=obj)
        serializer = ExportValueSerializer(instance=values, many=True)
        return serializer.data


class ExportSerializer(serializers.ModelSerializer):

    snapshots = ExportSnapshotSerializer(many=True)
    values = ExportValueSerializer(many=True)

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'catalog',
            'snapshots',
            'values'
        )

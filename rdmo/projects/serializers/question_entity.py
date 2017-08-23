from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from rdmo.core.serializers import MarkdownSerializerMixin
from rdmo.conditions.models import Condition
from rdmo.domain.models import AttributeEntity, Attribute, Range
from rdmo.options.models import OptionSet, Option

from rdmo.questions.models import QuestionEntity, Question


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'text',
            'additional_input'
        )


class OptionSetSerializer(serializers.ModelSerializer):

    options = OptionSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'options',
            'conditions'
        )


class RangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Range
        fields = (
            'id',
            'minimum',
            'maximum',
            'step'
        )


class AttributeSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    range = RangeSerializer(read_only=True)
    verbosename = serializers.SerializerMethodField()
    optionsets = OptionSetSerializer(many=True)

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


class AttributeEntitySerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

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


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'source',
            'relation',
            'target_text',
            'target_option'
        )


class QuestionSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('help', )

    attribute = AttributeSerializer(source='attribute_entity.attribute')

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

    collection = serializers.SerializerMethodField()

    questions = serializers.SerializerMethodField()

    next = serializers.SerializerMethodField()
    prev = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    section = serializers.SerializerMethodField()
    subsection = serializers.SerializerMethodField()

    conditions = ConditionSerializer(source='attribute_entity.conditions', many=True)

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'help',
            'collection',
            'is_set',
            'next',
            'prev',
            'progress',
            'section',
            'subsection',
            'collection',
            'questions',
            'conditions'
        )

    def get_questions(self, obj):
        if obj.is_set:
            return QuestionSerializer(instance=obj.questions, many=True, read_only=True).data
        else:
            return [QuestionSerializer(instance=obj.question, read_only=True).data]

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
            return AttributeEntitySerializer(instance=obj.attribute_entity.parent_collection).data
        elif obj.attribute_entity.is_collection and not obj.attribute_entity.is_attribute:
            return AttributeEntitySerializer(instance=obj.attribute_entity).data
        else:
            return None

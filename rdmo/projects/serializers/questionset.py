from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from rdmo.core.serializers import MarkdownSerializerMixin
from rdmo.conditions.models import Condition
from rdmo.domain.models import AttributeEntity, Attribute, Range
from rdmo.options.models import OptionSet, Option

from rdmo.questions.models import QuestionSet, Question


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

    class Meta:
        model = Attribute
        fields = (
            'id',
            'range',
            'verbosename'
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

    attribute = AttributeSerializer(source='attribute_entity.attribute', default=None)
    optionsets = OptionSetSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'order',
            'text',
            'help',
            'widget_type',
            'value_type',
            'unit',
            'attribute',
            'optionsets',
            'is_collection'
        )


class QuestionSetSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('help', )

    questions = QuestionSerializer(many=True)

    next = serializers.SerializerMethodField()
    prev = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    section = serializers.SerializerMethodField()
    subsection = serializers.SerializerMethodField()

    attribute_entity = AttributeEntitySerializer()

    conditions = ConditionSerializer(default=None, many=True)

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'help',
            'attribute_entity',
            'is_collection',
            'next',
            'prev',
            'progress',
            'section',
            'subsection',
            'questions',
            'conditions'
        )

    def get_prev(self, obj):
        try:
            return QuestionSet.objects.get_prev(obj.pk).pk
        except QuestionSet.DoesNotExist:
            return None

    def get_next(self, obj):
        try:
            return QuestionSet.objects.get_next(obj.pk).pk
        except QuestionSet.DoesNotExist:
            return None

    def get_progress(self, obj):
        try:
            return QuestionSet.objects.get_progress(obj.pk)
        except QuestionSet.DoesNotExist:
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

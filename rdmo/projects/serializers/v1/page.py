from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rdmo.conditions.models import Condition
from rdmo.core.serializers import MarkdownSerializerMixin
from rdmo.options.models import Option, OptionSet
from rdmo.questions.models import Page, Question, QuestionSet
from rdmo.questions.utils import get_widget_class


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
            'has_provider',
            'has_search',
            'has_refresh',
            'has_conditions'
        )


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

    conditions = ConditionSerializer(default=None, many=True)
    optionsets = serializers.SerializerMethodField()

    verbose_name = serializers.SerializerMethodField()
    verbose_name_plural = serializers.SerializerMethodField()
    widget_class = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'id',
            'help',
            'text',
            'default_text',
            'default_option',
            'default_external_id',
            'verbose_name',
            'verbose_name_plural',
            'widget_type',
            'widget_class',
            'value_type',
            'unit',
            'width',
            'minimum',
            'maximum',
            'step',
            'attribute',
            'conditions',
            'optionsets',
            'is_collection',
            'is_optional',
            'has_conditions'
        )

    def get_optionsets(self, obj):
        return OptionSetSerializer(obj.optionsets.order_by('order'), many=True).data

    def get_verbose_name(self, obj):
        return obj.verbose_name or _('item')

    def get_verbose_name_plural(self, obj):
        return obj.verbose_name_plural or _('items')

    def get_widget_class(self, obj):
        return get_widget_class(obj.widget_type)


class QuestionSetSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('help', )

    questionsets = serializers.SerializerMethodField()
    questions = QuestionSerializer(many=True)

    verbose_name = serializers.SerializerMethodField()
    verbose_name_plural = serializers.SerializerMethodField()

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
            'attribute',
            'is_collection',
            'questionsets',
            'questions',
            'has_conditions'
        )

    def get_questionsets(self, obj):
        return QuestionSetSerializer(obj.questionsets.all(), many=True, read_only=True).data

    def get_verbose_name(self, obj):
        return obj.verbose_name or _('set')

    def get_verbose_name_plural(self, obj):
        return obj.verbose_name_plural or _('sets')


class PageSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('help', )

    questionsets = QuestionSetSerializer(many=True)
    questions = QuestionSerializer(many=True)

    section = serializers.SerializerMethodField()
    prev_page = serializers.SerializerMethodField()
    next_page = serializers.SerializerMethodField()
    verbose_name = serializers.SerializerMethodField()
    verbose_name_plural = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = (
            'id',
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
            'attribute',
            'is_collection',
            'section',
            'prev_page',
            'next_page',
            'questionsets',
            'questions',
            'has_conditions'
        )

    def get_section(self, obj):
        section = self.context['catalog'].get_section_for_page(obj)
        return {
           'id': section.id,
           'title': section.title,
        } if section else {}

    def get_prev_page(self, obj):
        page = self.context['catalog'].get_prev_page(obj)
        return page.id if page else None

    def get_next_page(self, obj):
        page = self.context['catalog'].get_next_page(obj)
        return page.id if page else None

    def get_verbose_name(self, obj):
        return obj.verbose_name or _('set')

    def get_verbose_name_plural(self, obj):
        return obj.verbose_name_plural or _('sets')

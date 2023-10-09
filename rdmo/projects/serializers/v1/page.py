from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rdmo.conditions.models import Condition
from rdmo.core.serializers import ElementModelSerializerMixin, MarkdownSerializerMixin
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

    options = OptionSerializer(source='elements', many=True)

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


class QuestionSerializer(ElementModelSerializerMixin, MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('help', )

    model = serializers.SerializerMethodField()
    conditions = ConditionSerializer(default=None, many=True)
    optionsets = serializers.SerializerMethodField()

    verbose_name = serializers.SerializerMethodField()
    verbose_name_plural = serializers.SerializerMethodField()
    widget_class = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'id',
            'model',
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
        ordered_optionsets = sorted(obj.optionsets.all(), key=lambda optionset: optionset.order)
        return OptionSetSerializer(ordered_optionsets, many=True).data

    def get_verbose_name(self, obj):
        return obj.verbose_name or _('item')

    def get_verbose_name_plural(self, obj):
        return obj.verbose_name_plural or _('items')

    def get_widget_class(self, obj):
        return get_widget_class(obj.widget_type)


class QuestionSetSerializer(ElementModelSerializerMixin, MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('help', )

    model = serializers.SerializerMethodField()
    elements = serializers.SerializerMethodField()
    verbose_name = serializers.SerializerMethodField()
    verbose_name_plural = serializers.SerializerMethodField()

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'model',
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
            'attribute',
            'is_collection',
            'elements',
            'has_conditions'
        )

    def get_elements(self, obj):
        for element in obj.elements:
            if isinstance(element, QuestionSet):
                yield QuestionSetSerializer(element, context=self.context).data
            else:
                yield QuestionSerializer(element, context=self.context).data

    def get_verbose_name(self, obj):
        return obj.verbose_name or _('set')

    def get_verbose_name_plural(self, obj):
        return obj.verbose_name_plural or _('sets')


class PageSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('help', )

    elements = serializers.SerializerMethodField()
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
            'elements',
            'section',
            'prev_page',
            'next_page',
            'has_conditions'
        )

    def get_elements(self, obj):
        for element in obj.elements:
            if isinstance(element, QuestionSet):
                yield QuestionSetSerializer(element, context=self.context).data
            else:
                yield QuestionSerializer(element, context=self.context).data

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

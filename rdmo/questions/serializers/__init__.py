from rest_framework import serializers

from rdmo.domain.models import Attribute
from rdmo.options.models import OptionSet
from rdmo.conditions.models import Condition

from ..models import Catalog, Section, QuestionSet, Question
from ..validators import (
    CatalogUniqueKeyValidator,
    SectionUniquePathValidator,
    QuestionSetUniquePathValidator,
    QuestionUniquePathValidator
)


class CatalogIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = (
            'id',
            'title',
            'key'
        )


class CatalogSerializer(serializers.ModelSerializer):

    key = serializers.CharField(required=True)

    class Meta:
        model = Catalog
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'title',
            'title_en',
            'title_de'
        )
        validators = (CatalogUniqueKeyValidator(), )


class SectionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'path',
        )


class SectionSerializer(serializers.ModelSerializer):

    key = serializers.CharField(required=True)

    class Meta:
        model = Section
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'catalog',
            'order',
            'title',
            'title_en',
            'title_de'
        )
        validators = (SectionUniquePathValidator(), )


class QuestionSetIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'path'
        )


class QuestionSetSerializer(serializers.ModelSerializer):

    key = serializers.CharField(required=True)

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'attribute',
            'section',
            'is_collection',
            'order',
            'title_en',
            'title_de',
            'help_en',
            'help_de',
            'verbose_name_en',
            'verbose_name_plural_en',
            'verbose_name_de',
            'verbose_name_plural_de',
            'conditions'
        )
        validators = (QuestionSetUniquePathValidator(), )


class QuestionSerializer(serializers.ModelSerializer):

    key = serializers.CharField(required=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'attribute',
            'questionset',
            'is_collection',
            'order',
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'verbose_name_en',
            'verbose_name_plural_en',
            'verbose_name_de',
            'verbose_name_plural_de',
            'maximum',
            'minimum',
            'step',
            'widget_type',
            'value_type',
            'unit',
            'optionsets',
            'conditions'
        )
        validators = (QuestionUniquePathValidator(), )


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'path'
        )


class OptionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'key'
        )


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'key'
        )

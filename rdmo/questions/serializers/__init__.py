from rest_framework import serializers

from rdmo.domain.models import AttributeEntity, Attribute
from rdmo.options.models import OptionSet
from rdmo.conditions.models import Condition

from ..models import Catalog, Section, Subsection, QuestionSet, Question
from ..validators import (
    CatalogUniqueKeyValidator,
    SectionUniquePathValidator,
    SubsectionUniquePathValidator,
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


class SubsectionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subsection
        fields = (
            'id',
            'path',
        )


class SubsectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subsection
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'section',
            'order',
            'title',
            'title_en',
            'title_de',
        )
        validators = (SubsectionUniquePathValidator(), )


class QuestionSetIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'path'
        )


class QuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'attribute_entity',
            'subsection',
            'is_collection',
            'order',
            'help_en',
            'help_de',
            'conditions'
        )
        validators = (QuestionSetUniquePathValidator(), )


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'attribute_entity',
            'subsection',
            'parent',
            'is_collection',
            'order',
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'widget_type',
            'value_type',
            'unit',
            'optionsets',
            'conditions'
        )
        validators = (QuestionUniquePathValidator(), )


class AttributeEntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'path'
        )


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

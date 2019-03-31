from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin

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


class CatalogSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    key = serializers.CharField(required=True)

    class Meta:
        model = Catalog
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'order',
        )
        trans_fields = (
            'title',
        )
        validators = (CatalogUniqueKeyValidator(), )


class SectionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'path',
        )


class SectionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

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
        )
        trans_fields = (
            'title',
        )
        validators = (SectionUniquePathValidator(), )


class QuestionSetIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'path'
        )


class QuestionSetSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

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
            'conditions',
        )
        trans_fields = (
            'title',
            'help',
            'verbose_name',
            'verbose_name_plural',
        )
        validators = (QuestionSetUniquePathValidator(), )


class QuestionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

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
            'maximum',
            'minimum',
            'step',
            'widget_type',
            'value_type',
            'unit',
            'optionsets',
            'conditions'
        )
        trans_fields = (
            'text',
            'help',
            'verbose_name',
            'verbose_name_plural',
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

from rest_framework import serializers

from rdmo.domain.models import AttributeEntity, Attribute

from ..models import Catalog, Section, Subsection, QuestionEntity, Question
from ..validators import (
    CatalogUniqueKeyValidator,
    SectionUniquePathValidator,
    SubsectionUniquePathValidator,
    QuestionEntityUniquePathValidator,
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
        model = QuestionEntity
        fields = (
            'id',
            'path'
        )


class QuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'subsection',
            'attribute_entity',
            'order',
            'help_en',
            'help_de',
        )
        validators = (QuestionEntityUniquePathValidator(), )


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'subsection',
            'parent',
            'attribute_entity',
            'order',
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'widget_type',
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

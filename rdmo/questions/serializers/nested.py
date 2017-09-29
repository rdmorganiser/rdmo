from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse

from rdmo.domain.models import AttributeEntity

from ..models import Catalog, Section, Subsection, QuestionEntity, Question


class AttributeEntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'path'
        )


class QuestionSerializer(serializers.ModelSerializer):

    attribute_entity = AttributeEntitySerializer(read_only=True)

    warning = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'id',
            'path',
            'text',
            'attribute_entity',
            'warning'
        )

    def get_warning(self, obj):
        if not obj.attribute_entity:
            return _('No attribute selected.')
        else:
            return None


class QuestionEntitySerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True, read_only=True)
    text = serializers.CharField(source='question.text')

    attribute_entity = AttributeEntitySerializer(read_only=True)

    warning = serializers.SerializerMethodField()

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'path',
            'subsection',
            'text',
            'is_set',
            'attribute_entity',
            'questions',
            'warning'
        )

    def get_warning(self, obj):
        if obj.is_set:
            if not obj.attribute_entity:
                return _('No entity selected.')
            else:
                descendants = obj.attribute_entity.get_descendants()

                for question in obj.questions.all():
                    if question.attribute_entity and question.attribute_entity not in descendants:
                        return _('Entity and questions attributes mismatch.')
                        break

                return None
        else:
            if not obj.attribute_entity:
                return _('No attribute selected.')
            else:
                return None


class SubsectionSerializer(serializers.ModelSerializer):

    entities = serializers.SerializerMethodField()

    class Meta:
        model = Subsection
        fields = (
            'id',
            'path',
            'title',
            'entities'
        )

    def get_entities(self, obj):
        entities = QuestionEntity.objects.filter(subsection=obj, question__parent=None).order_by('order')
        serializer = QuestionEntitySerializer(instance=entities, many=True)
        return serializer.data


class SectionSerializer(serializers.ModelSerializer):

    subsections = SubsectionSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = (
            'id',
            'path',
            'title',
            'subsections'
        )


class CatalogSerializer(serializers.ModelSerializer):

    sections = SectionSerializer(many=True, read_only=True)

    urls = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = (
            'id',
            'key',
            'title',
            'title_en',
            'title_de',
            'sections',
            'urls'
        )

    def get_urls(self, obj):
        urls = {
            'xml': reverse('questions_catalog_export', args=[obj.pk, 'xml'])
        }
        for key, text in settings.EXPORT_FORMATS:
            urls[key] = reverse('questions_catalog_export', args=[obj.pk, key])
        return urls

from rest_framework import serializers

from apps.domain.models import AttributeSet, Attribute

from .models import *


class NestedOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = ('id', 'key', 'text', 'text_en', 'text_de')


class NestedAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = ('id', 'tag')


class NestedAttributeSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeSet
        fields = ('id', 'tag')


class NestedQuestionSerializer(serializers.ModelSerializer):

    attribute = NestedAttributeSerializer(read_only=True)

    options = NestedOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'attribute', 'widget_type', 'is_collection', 'options')


class NestedQuestionEntitySerializer(serializers.ModelSerializer):

    questions = NestedQuestionSerializer(source='questionset.questions', many=True, read_only=True)
    text = serializers.CharField(source='question.text')

    attribute = NestedAttributeSerializer(source='question.attribute', read_only=True)
    attributeset = NestedAttributeSetSerializer(source='questionset.attributeset', read_only=True)

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'title',
            'text',
            'is_set',
            'is_collection',
            'attribute',
            'attributeset',
            'questions'
        )


class NestedSubsectionSerializer(serializers.ModelSerializer):

    entities = serializers.SerializerMethodField()

    class Meta:
        model = Subsection
        fields = ('id', 'title', 'entities')

    def get_entities(self, obj):
        entities = QuestionEntity.objects.filter(subsection=obj, question__questionset=None)
        serializer = NestedQuestionEntitySerializer(instance=entities, many=True)
        return serializer.data


class NestedSectionSerializer(serializers.ModelSerializer):

    subsections = NestedSubsectionSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ('id', 'title', 'subsections')


class NestedCatalogSerializer(serializers.ModelSerializer):

    sections = NestedSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = ('id', 'title', 'title_en', 'title_de', 'sections')


class CatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = ('id', 'title', 'title_en', 'title_de')


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'catalog',
            'order',
            'title_en',
            'title_de'
        )


class SubsectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subsection
        fields = (
            'id',
            'section',
            'order',
            'title_en',
            'title_de'
        )


class QuestionEntitySerializer(serializers.ModelSerializer):

    questions = NestedQuestionSerializer(source='questionset.questions', many=True, read_only=True)
    text = serializers.CharField(source='question.text')
    widget_type = serializers.CharField(source='question.widget_type')

    next = serializers.SerializerMethodField()
    prev = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    attribute = NestedAttributeSerializer(source='question.attribute', read_only=True)
    attributeset = NestedAttributeSetSerializer(source='questionset.attributeset', read_only=True)

    options = NestedOptionSerializer(source='question.options', many=True, read_only=True)

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'title',
            'text',
            'help',
            'is_set',
            'is_collection',
            'tag',
            'questions',
            'widget_type',
            'next',
            'prev',
            'progress',
            'attribute',
            'attributeset',
            'options'
        )

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


class QuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'subsection',
            'order',
            'title_en',
            'title_de',
            'help_en',
            'help_de',
            'attributeset'
        )


class QuestionSerializer(serializers.ModelSerializer):

    options = NestedOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'subsection',
            'order',
            'title_en',
            'title_de',
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'attribute',
            'questionset',
            'widget_type',
            'options'
        )


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = ('id', 'key', 'text', 'text_en', 'text_de')


class WidgetTypeSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj[0]

    def get_text(self, obj):
        return obj[1]

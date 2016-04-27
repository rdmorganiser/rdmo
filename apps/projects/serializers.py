from rest_framework import serializers

from .models import *


class ProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'current_snapshot', 'catalog')


class ValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Value
        fields = ('id', 'index', 'created', 'updated', 'text', 'snapshot', 'attribute', 'valueset')


class ValueSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = ValueSet
        fields = ('id', 'index', 'created', 'updated', 'snapshot', 'attributeset')


class ValueEntitySerializer(serializers.ModelSerializer):

    values = ValueSerializer(source='valueset.values', many=True, read_only=True)
    text = serializers.CharField(source='value.text')

    attribute = serializers.IntegerField(source='value.attribute.pk')
    attributeset = serializers.IntegerField(source='valueset.attributeset.pk')

    class Meta:
        model = ValueEntity
        fields = ('id', 'index', 'created', 'updated', 'text', 'snapshot', 'values', 'attribute', 'attributeset')

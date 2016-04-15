from rest_framework import serializers

from .models import *


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = ('id', 'tag', 'is_collection', 'attributeset')


class AttributeSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeSet
        fields = ('id', 'tag', 'is_collection')


class AttributeEntitySerializer(serializers.ModelSerializer):

    attributes = AttributeSerializer(source='attributeset.attributes', many=True, read_only=True)
    attributeset = serializers.NullBooleanField()

    class Meta:
        model = AttributeEntity
        fields = ('id', 'tag', 'is_collection', 'is_set', 'attributes', 'attributeset')

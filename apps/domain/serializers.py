from rest_framework import serializers

from .models import *


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = ('id', 'tag', 'text', 'is_collection', 'attributeset', 'value_type')


class AttributeSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeSet
        fields = ('id', 'tag', 'text', 'is_collection')


class AttributeEntitySerializer(serializers.ModelSerializer):

    attributes = AttributeSerializer(source='attributeset.attributes', many=True, read_only=True)
    attributeset = serializers.NullBooleanField()

    class Meta:
        model = AttributeEntity
        fields = ('id', 'tag', 'text', 'is_collection', 'is_set', 'attributes', 'attributeset')


class ValueTypeSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj[0]

    def get_text(self, obj):
        return obj[1]

from rest_framework import serializers

from .models import *


class OptionSetIndexOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'title',
            'text'
        )


class OptionSetIndexSerializer(serializers.ModelSerializer):

    options = OptionSetIndexOptionsSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'title',
            'options'
        )


class OptionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'title',
            'order'
        )


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'optionset',
            'title',
            'order',
            'text_en',
            'text_de',
            'additional_input'
        )

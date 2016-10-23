from rest_framework import serializers

from .models import *


class OptionSetIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSet
        fields = (
            'id',
        )


class OptionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
        )


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
        )

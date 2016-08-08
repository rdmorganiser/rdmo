from rest_framework import serializers

from .models import *


class ViewIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = View
        fields = (
            'id',
            'title',
            'description',
        )


class ViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = View
        fields = (
            'id',
            'title',
            'description',
        )

from rest_framework import serializers

from .models import *


class ProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'current_snapshot', 'catalog')


class ValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Value
        fields = (
            'id',
            'snapshot',
            'attribute',
            'set_index',
            'collection_index',
            'text',
            'option'
        )

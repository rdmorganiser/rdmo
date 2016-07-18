from rest_framework import serializers

from .models import *


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            '__str__',
            'attribute',
            'time_period',
            'title',
            'title_en',
            'title_de',
            'text',
            'text_en',
            'text_de',
        )

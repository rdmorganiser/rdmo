from django.template import Template, TemplateSyntaxError

from rest_framework import serializers
from rest_framework import exceptions

from .models import *


class ViewIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = View
        fields = (
            'id',
            'title',
            'description'
        )


class ViewSerializer(serializers.ModelSerializer):

    def validate(self, data):
        # try to render the tamplate to see that the syntax is ok
        try:
            Template(data['template']).render(Context({}))
        except TemplateSyntaxError as e:
            raise exceptions.ValidationError({'template': [e.message]})

        return super(ViewSerializer, self).validate(data)

    class Meta:
        model = View
        fields = (
            'id',
            'title',
            'description',
            'template'
        )

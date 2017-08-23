from rest_framework import serializers

from ..models import View


class ViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = View
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'title_en',
            'title_de',
            'help_en',
            'help_de',
            'template'
        )

from rest_framework import serializers

from ..models import Attribute


class AttributeSerializer(serializers.ModelSerializer):

    parent = serializers.HyperlinkedRelatedField(view_name='api-v1-domain:attribute-detail', read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'path',
            'key',
            'comment',
            'parent',
            'children'
        )

    def get_children(self, obj):

        children = []
        for child in obj.get_children():
            field = serializers.HyperlinkedRelatedField(view_name='api-v1-domain:attribute-detail', read_only=True)

            # bind the field to the serializer
            # this is needed to have the context (and the request availabe in the field)
            field.bind(child.key, self)

            children.append(field.to_representation(child))

        return children

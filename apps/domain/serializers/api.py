from rest_framework import serializers

from ..models import AttributeEntity, Attribute, Range, VerboseName


class RangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Range
        fields = (
            'id',
            'minimum',
            'maximum',
            'step'
        )


class VerboseNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerboseName
        fields = (
            'id',
            'name_en',
            'name_de',
            'name_plural_en',
            'name_plural_de'
        )


class AttributeEntitySerializer(serializers.ModelSerializer):

    verbose_name = VerboseNameSerializer(read_only=True)
    conditions = serializers.HyperlinkedRelatedField(view_name='api-v1-conditions:condition-detail', read_only=True, many=True)
    parent = serializers.HyperlinkedRelatedField(view_name='api-v1-domain:entity-detail', read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'path',
            'key',
            'comment',
            'is_collection',
            'verbose_name',
            'conditions',
            'parent',
            'children'
        )

    def get_children(self, obj):

        children = []
        for child in obj.get_children():
            if child.is_attribute:
                field = serializers.HyperlinkedRelatedField(view_name='api-v1-domain:attribute-detail', read_only=True)
            else:
                field = serializers.HyperlinkedRelatedField(view_name='api-v1-domain:entity-detail', read_only=True)

            field.context = self.context
            children.append(field.to_representation(child))

        return children


class AttributeSerializer(serializers.ModelSerializer):

    range = RangeSerializer(read_only=True)
    verbose_name = VerboseNameSerializer(read_only=True)
    optionsets = serializers.HyperlinkedRelatedField(view_name='api-v1-options:optionset-detail', read_only=True, many=True)
    conditions = serializers.HyperlinkedRelatedField(view_name='api-v1-conditions:condition-detail', read_only=True, many=True)
    parent = serializers.HyperlinkedRelatedField(view_name='api-v1-domain:entity-detail', read_only=True)

    class Meta:
        model = Attribute
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'path',
            'key',
            'comment',
            'value_type',
            'unit',
            'is_collection',
            'range',
            'verbose_name',
            'optionsets',
            'conditions',
            'parent'
        )

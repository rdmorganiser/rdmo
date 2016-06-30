from markdown import markdown as markdown_function

from django.utils.encoding import force_text

from rest_framework import serializers


class RecursiveField(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ChoicesSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj[0]

    def get_text(self, obj):
        return obj[1]


class MarkdownSerializerMixin(serializers.Serializer):

    markdown_fields = ()

    def to_representation(self, instance):
        response = super(MarkdownSerializerMixin, self).to_representation(instance)

        for markdown_field in self.markdown_fields:
            if markdown_field in response and response[markdown_field]:
                response[markdown_field] = markdown_function(force_text(response[markdown_field]))

        return response

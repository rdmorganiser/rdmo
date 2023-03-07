from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from rest_framework import serializers
from rest_framework.utils import model_meta

from rdmo.core.utils import get_languages, markdown2html


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
                response[markdown_field] = markdown2html(response[markdown_field])

        return response


class TranslationSerializerMixin(object):

    def __init__(self, *args, **kwargs):
        super(TranslationSerializerMixin, self).__init__(*args, **kwargs)

        meta = getattr(self, 'Meta', None)
        if meta:
            for lang_code, lang_string, lang_field in get_languages():
                for field in meta.trans_fields:
                    field_name = '%s_%s' % (field, lang_field)
                    model_field = meta.model._meta.get_field(field_name)

                    self.fields['%s_%s' % (field, lang_code)] = serializers.CharField(
                        source=field_name,
                        required=not model_field.blank,
                        allow_null=model_field.null,
                        allow_blank=model_field.blank)


class ThroughModelListField(serializers.ListField):

    def to_internal_value(self, data):
        target_field_name = self.child.Meta.fields[0]
        return super().to_internal_value([
            {
                target_field_name: value
            } for value in data
        ])

    def to_representation(self, data):
        target_field_name = self.child.Meta.fields[0]
        items = sorted(data.all(), key=lambda e: e.order)
        return [getattr(item, target_field_name).id for item in items]


class ThroughModelSerializerMixin(object):

    def create(self, validated_data):
        through_fields = self.get_through_fields(validated_data)
        instance = super().create(validated_data)
        instance = self.set_through_fields(instance, through_fields)
        return instance

    def update(self, instance, validated_data):
        through_fields = self.get_through_fields(validated_data)
        instance = super().update(instance, validated_data)
        instance = self.set_through_fields(instance, through_fields)
        return instance

    def get_through_fields(self, validated_data):
        model_info = model_meta.get_field_info(self.Meta.model)

        through_fields = {}
        for field_name, field in self.get_fields().items():
            if isinstance(field, ThroughModelListField):
                through_model = model_info.reverse_relations[field.source].related_model

                target_field_name = field.child.Meta.fields[0]
                for fn, f in model_meta.get_field_info(through_model).forward_relations.items():
                    if fn != target_field_name:
                        source_field_name = fn

                through_fields[field.source] = {
                    'source_field_name': source_field_name,
                    'target_field_name': target_field_name,
                    'through_model': through_model,
                    'validated_data': validated_data.pop(field.source, None)
                }

        return through_fields

    def set_through_fields(self, instance, through_fields):
        for field_name, field_config in through_fields.items():
            if field_config['validated_data'] is not None:
                items = list(getattr(instance, field_name).all())

                for order, data in enumerate(field_config['validated_data']):
                    try:
                        # look for the item in items
                        item = next(filter(lambda item: getattr(item, field_config['target_field_name']) ==
                                           data.get(field_config['target_field_name']), items))
                        # update order if the item if it changed
                        if item.order != order:
                            item.order = order
                            item.save()

                        # remove the item from the items list so that it won't get removed
                        items.remove(item)
                    except StopIteration:
                        # create a new item
                        new_data = dict({
                            field_config['source_field_name']: instance,
                            'order': order
                        }, **data)
                        new_item = field_config['through_model'](**new_data)
                        new_item.save()

                # remove the remainders of the items list
                for item in items:
                    item.delete()

        return instance


class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = (
            'id',
            'domain',
            'name'
        )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            'id',
            'name'
        )
